const {test, assert, insp} = require('scar');
const reqlib = require('../../../util/reqlib');
const {parsePattern} = reqlib('util');

test('util.parsePattern()', () => {
    assert.equal(typeof parsePattern, 'function', 'is function');

    [
        ['', false, ''],
        [' ', false, '\\ '],
        ['a', false, 'a'],
        ['ä', false, 'ä'],
        ['á', false, 'á'],
        ['*', false, '\\*'],
        ['ab', false, 'ab'],
        ['rea', false, 'rea'],
        ['re:', false, 're:'],
        ['re:a', false, 're:a'],
        ['a b', false, 'a\\ b'],
        ['ab c', false, 'ab\\ c'],
        [' a ', false, '\\ a\\ '],

        ['', true, ''],
        [' ', true, ''],
        ['a', true, 'a'],
        ['ä', true, 'ä'],
        ['á', true, 'á'],
        ['*', true, '\\*'],
        ['ab', true, 'a.*?b'],
        ['rea', true, 'r.*?e.*?a'],
        [' re:', true, 'r.*?e.*?:'],
        ['are:', true, 'a.*?r.*?e.*?:'],
        ['re:', true, ''],
        ['re:a', true, 'a'],
        ['a b', true, 'a|b'],
        ['ab c', true, 'a.*?b|c'],
        [' a ', true, 'a']
    ].forEach(([pattern, advanced, exp], idx) => {
        assert.equal(parsePattern(pattern, advanced), exp, `fix#${idx} - (${insp(pattern)}, ${insp(advanced)}) -> ${insp(exp)}`);
    });
});

test('util.parsePattern() invalid expression', () => {
    // a `re:` pattern that is not a valid regular expression falls back to the typed text, matched literally
    [
        ['re:(', 're:\\('],
        ['re:[', 're:\\['],
        ['re:*a', 're:\\*a'],
        ['re:a{2,1}', 're:a\\{2\\,1\\}']
    ].forEach(([typed, exp]) => {
        // a throw here fails the test
        const pattern = parsePattern(typed, true);
        assert.equal(pattern, exp, `literal fallback for ${insp(typed)}`);
        assert.equal(new RegExp(pattern, 'i').test(typed), true, `${insp(typed)} matches itself`);
    });

    assert.equal(parsePattern('re:^a.*b$', true), '^a.*b$', 'valid expression is kept');
});
