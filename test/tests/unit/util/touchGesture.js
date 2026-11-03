const {test, assert} = require('scar');
const reqlib = require('../../../util/reqlib');
const {touchGesture} = reqlib('util');

test('util.touchGesture()', () => {
    assert.equal(typeof touchGesture, 'function', 'is function');

    [
        // dx, dy, dt, expected
        [0, 0, 80, 'tap'],
        [8, -12, 120, 'tap'],
        [0, 0, 600, null], // a long press is no tap
        [-120, 10, 200, 'next'],
        [120, -10, 200, 'prev'],
        [-40, 0, 200, 'next'],
        [-39, 0, 200, null], // too short
        [-120, 0, 800, null], // too slow, a drag
        [-120, 70, 200, null], // diagonal
        [10, 200, 200, null], // vertical scroll
        [30, 150, 200, null],
        [-60, 29, 200, 'next'] // some drift is fine
    ].forEach(([dx, dy, dt, expected]) => {
        assert.equal(touchGesture(dx, dy, dt), expected, `${dx},${dy},${dt}`);
    });
});
