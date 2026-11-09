// Boots the built scripts.js in jsdom against a stubbed API, so a bundle that
// cannot start in a browser fails here instead of shipping a blank page.
const assert = require('assert');
const fs = require('fs');
const {join} = require('path');
const vm = require('vm');
const {JSDOM, VirtualConsole} = require('jsdom');

const H5AI = join(__dirname, '../build/_h5ai');
const read_conf = name => vm.runInNewContext(`(${fs.readFileSync(join(H5AI, 'private/conf', name), 'utf8')})`);

const responses = {
    setup: {
        setup: {PUBLIC_HREF: '/_h5ai/public/', ROOT_HREF: '/', H5AI_HREF: '/_h5ai/', HAS_SERVER: true},
        options: read_conf('options.json'),
        types: read_conf('types.json'),
        theme: {},
        langs: {}
    },
    items: {items: [{href: '/', time: 0, size: 0, managed: true, fetched: true}]},
    // a markdown header goes through the bundled marked
    custom: {custom: {header: {content: '# Header', type: 'md'}, footer: {content: null}}}
};

const errors = [];
const requests = [];
const virtualConsole = new VirtualConsole();
virtualConsole.on('jsdomError', err => errors.push(err.detail || err.message));
process.on('unhandledRejection', err => errors.push(err));

const html = '<!DOCTYPE html><html class="no-js"><head></head><body id="root" class="index">' +
    '<div id="fallback-hints"></div><div id="fallback"></div><script data-module="index"></script></body></html>';
const {window} = new JSDOM(html, {
    url: 'http://localhost/',
    runScripts: 'outside-only',
    pretendToBeVisual: true,
    virtualConsole,
    beforeParse(win) {
        // jsdom has no document.domain; browsers return the host
        Reflect.defineProperty(win.document, 'domain', {value: 'localhost'});
        // jsdom has no canvas; bundled kjua probes a 2d context on load
        win.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {get: () => () => 1});
        win.HTMLCanvasElement.prototype.toDataURL = () => 'data:,';
        // jsdom has no CSS.supports; answer as a browser that meets the build target
        win.CSS = {supports: () => true};
        win.XMLHttpRequest = class {
            open() {}
            setRequestHeader() {}
            send(body) {
                const query = JSON.parse(body);
                requests.push(query);
                this.readyState = 4;
                this.responseText = JSON.stringify(query.setup ? responses.setup : query.custom ? responses.custom : responses.items);
                setTimeout(() => this.onreadystatechange(), 0);
            }
        };
        win.XMLHttpRequest.DONE = 4;
    }
});

try {
    window.eval(fs.readFileSync(join(H5AI, 'public/js/scripts.js'), 'utf8'));
} catch (err) {
    errors.push(err);
}

setTimeout(() => {
    assert.deepStrictEqual(errors, [], 'bundle raised errors');
    assert.ok(requests.length && requests[0].setup, 'bundle did not request its setup');
    assert.ok(window.document.querySelector('#view'), 'bundle did not render #view');
    assert.ok(window.document.querySelector('#content-header h1'), 'bundle did not render the markdown header');
    console.log('bundle boots');
    window.close();
}, 500);
