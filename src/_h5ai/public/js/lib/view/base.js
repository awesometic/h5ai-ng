const {dom} = require('../util');

const SEL_ROOT = 'body';
const TPL_TOPBAR =
        `<header id="topbar">
            <div id="toolbar"></div>
            <div id="flowbar"></div>
            <a id="backlink" href="https://github.com/awesometic/h5ai-ng" title="powered by h5ai-ng - https://github.com/awesometic/h5ai-ng - based on h5ai by Lars Jung (https://larsjung.de/h5ai/)">
                <div>powered</div>
                <div>by h5ai-ng</div>
            </a>
        </header>`;
const TPL_MAINROW =
        `<div id="mainrow">
            <main id="content"></main>
        </div>`;

const init = () => {
    const $root = dom(SEL_ROOT)
        .attr('id', 'root')
        .clr()
        .app(TPL_TOPBAR)
        .app(TPL_MAINROW);

    return {
        $root,
        $topbar: $root.find('#topbar'),
        $toolbar: $root.find('#toolbar'),
        $flowbar: $root.find('#flowbar'),
        $mainrow: $root.find('#mainrow'),
        $content: $root.find('#content')
    };
};

module.exports = init();
