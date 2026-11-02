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

module.exports = {
    parsePattern: parse_pattern
};
