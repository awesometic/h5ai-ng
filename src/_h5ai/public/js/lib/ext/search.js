const {map, debounce, parsePattern, dom} = require('../util');
const server = require('../server');
const event = require('../core/event');
const location = require('../core/location');
const resource = require('../core/resource');
const allsettings = require('../core/settings');
const Item = require('../model/item');
const view = require('../view/view');


const settings = Object.assign({
    enabled: false,
    advanced: false,
    debounceTime: 300,
    ignorecase: true
}, allsettings.search);
const tpl =
        `<div id="search" class="tool">
            <img class="l10n_lb-search" src="${resource.image('search')}" alt="search"/>
            <input class="l10n_ph-search l10n_lb-search" type="text" value=""/>
        </div>`;
let inputIsVisible = false;
let prevPattern = '';
let $search;
let $input;
let $btn;


const search = (pattern = '') => {
    if (pattern === prevPattern) {
        return;
    }
    prevPattern = pattern;

    if (!pattern) {
        view.setLocation();
        return;
    }

    $search.addCls('pending');

    server.request({
        action: 'get',
        search: {
            href: location.getAbsHref(),
            pattern,
            ignorecase: settings.ignorecase
        }
    }).then(response => {
        $search.rmCls('pending');
        view.setHint('noMatch');
        view.setItems(map(response.search, item => Item.get(item)));
    });
};

const update = () => {
    if (inputIsVisible) {
        $search.addCls('active');
        $btn.attr('aria-expanded', 'true');
        $input[0].focus();
        search(parsePattern($input.val(), settings.advanced));
    } else {
        search();
        $search.rmCls('active');
        $btn.attr('aria-expanded', 'false');
    }
};

const toggle = () => {
    inputIsVisible = !inputIsVisible;
    update();
};

const reset = () => {
    inputIsVisible = false;
    $input.val('');
    update();
};

const init = () => {
    if (!settings.enabled) {
        return;
    }

    $search = dom(tpl).appTo('#toolbar');
    $input = $search.find('input');

    $btn = $search.find('img').btn().attr('aria-expanded', 'false').on('click', toggle);
    $input.on('keyup', debounce(update, settings.debounceTime));
    event.sub('location.changed', reset);
};


init();
