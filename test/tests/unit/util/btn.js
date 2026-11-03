const {test, assert} = require('scar');
const reqlib = require('../../../util/reqlib');
const {dom} = reqlib('util');

const press = (el, key) => {
    const ev = new global.window.KeyboardEvent('keydown', {key, bubbles: true, cancelable: true});
    el.dispatchEvent(ev);
    return ev;
};

test('util.dom.btn()', () => {
    const $parent = dom('<div><span></span></div>');
    const $el = $parent.find('span').btn();
    let clicks = 0;
    let bubbled = 0;
    $el.on('click', () => {clicks += 1;});
    $parent.on('keydown', () => {bubbled += 1;});

    assert.equal($el.attr('role'), 'button', 'role');
    assert.equal($el.attr('tabindex'), '0', 'focusable');

    assert.equal(press($el[0], 'Enter').defaultPrevented, true, 'Enter is consumed');
    assert.equal(press($el[0], ' ').defaultPrevented, true, 'Space is consumed');
    assert.equal(clicks, 2, 'Enter and Space click once each');
    assert.equal(bubbled, 0, 'handled keys do not reach ancestors');

    assert.equal(press($el[0], 'Tab').defaultPrevented, false, 'Tab is left alone');
    assert.equal(press($el[0], 'a').defaultPrevented, false, 'other keys are left alone');
    assert.equal(clicks, 2, 'other keys do not click');
    assert.equal(bubbled, 2, 'other keys still bubble');
});
