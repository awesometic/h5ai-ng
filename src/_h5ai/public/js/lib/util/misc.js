const esc_pattern = sequence => {
    return sequence.replace(/[\-\[\]{}()*+?.,\\$\^|#\s]/g, '\\$&');
};

const parse_pattern = (sequence, advanced) => {
    if (!advanced) {
        return esc_pattern(sequence);
    }

    if (sequence.substr(0, 3) === 're:') {
        const re = sequence.substr(3);
        try {
            RegExp(re);
            return re;
        } catch (err) {
            // not a valid expression (yet): match the typed text literally, so filter and search stay usable
            return esc_pattern(sequence);
        }
    }

    return sequence.trim().split(/\s+/).map(part => {
        return part.split('').map(char => esc_pattern(char)).join('.*?');
    }).join('|');
};

// classifies a one-finger touch by how far (px) and how long (ms) it moved
const touch_gesture = (dx, dy, dt) => {
    if (Math.abs(dx) <= 20 && Math.abs(dy) <= 20) {
        return dt <= 300 ? 'tap' : null;
    }
    // mostly horizontal, so a vertical scroll that drifts sideways is not a swipe
    if (Math.abs(dx) >= 40 && Math.abs(dx) >= 2 * Math.abs(dy) && dt <= 500) {
        return dx < 0 ? 'next' : 'prev';
    }
    return null;
};

module.exports = {
    parsePattern: parse_pattern,
    touchGesture: touch_gesture
};
