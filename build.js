const {execFileSync} = require('child_process');
const fs = require('fs');
const {join} = require('path');
const esbuild = require('esbuild');
const less = require('less');
const pug = require('pug');

const ROOT = __dirname;
const SRC = join(ROOT, 'src');
const BUILD = join(ROOT, 'build');
const H5AI = join(BUILD, '_h5ai');
const TARGET = ['chrome91', 'edge91', 'firefox90', 'safari15'];

const get_version = version => {
    try {
        const out = execFileSync('git', ['rev-list', `v${version}..HEAD`], {cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore']});
        const hashes = out.toString().split(/\r?\n/).filter(x => x);
        if (hashes.length) {
            return `${version}+${String(hashes.length).padStart(3, '0')}~${hashes[0].slice(0, 7)}`;
        }
    } catch (err) {
        // no git or no release tag: use the plain version
    }
    return version;
};

const build = async () => {
    const pkg = Object.assign({}, require('./package.json'));
    pkg.version = get_version(pkg.version);
    const comment = `${pkg.name} v${pkg.version} - ${pkg.homepage}`;
    const banner = `/* ${comment} */\n`;
    console.log(comment);

    fs.rmSync(BUILD, {recursive: true, force: true});
    fs.cpSync(join(SRC, '_h5ai'), H5AI, {recursive: true, filter: src => !(/\.(js|less|pug)$/).test(src)});
    ['README.md', 'CHANGELOG.md'].forEach(name => fs.copyFileSync(join(ROOT, name), join(H5AI, name)));

    const conf = join(H5AI, 'private/conf');
    fs.readdirSync(conf).filter(name => name.endsWith('.json')).forEach(name => {
        const file = join(conf, name);
        fs.writeFileSync(file, banner + fs.readFileSync(file, 'utf8'));
    });

    const index_php = join(H5AI, 'public/index.php');
    fs.writeFileSync(index_php, fs.readFileSync(index_php, 'utf8').replace('{{VERSION}}', pkg.version));

    const js = join(SRC, '_h5ai/public/js');
    await esbuild.build({
        entryPoints: [join(js, 'scripts.js')],
        outfile: join(H5AI, 'public/js/scripts.js'),
        bundle: true,
        minify: true,
        format: 'iife',
        target: TARGET,
        define: {global: 'globalThis'},
        banner: {js: banner + fs.readFileSync(join(js, 'pre.js'), 'utf8')}
    });

    const styles = join(SRC, '_h5ai/public/css/styles.less');
    const {css} = await less.render(fs.readFileSync(styles, 'utf8'), {
        filename: styles,
        math: 'always',
        paths: [join(ROOT, 'node_modules')]
    });
    const min = await esbuild.transform(css, {loader: 'css', minify: true, target: TARGET, banner});
    fs.writeFileSync(join(H5AI, 'public/css/styles.css'), min.code);

    const pages = join(SRC, '_h5ai/private/php/pages');
    fs.readdirSync(pages).filter(name => name.endsWith('.php.pug')).forEach(name => {
        const html = pug.renderFile(join(pages, name), {pkg});
        fs.writeFileSync(join(H5AI, 'private/php/pages', name.slice(0, -4)), `${html}<!-- ${comment} -->`);
    });

    // source-only folders (js/lib, css/lib) are left empty by the copy
    fs.readdirSync(H5AI, {recursive: true}).map(rel => join(H5AI, rel)).sort().reverse().forEach(path => {
        if (fs.statSync(path).isDirectory() && !fs.readdirSync(path).length) {
            fs.rmdirSync(path);
        }
    });
};

build().catch(err => {
    console.error(err);
    process.exitCode = 1;
});
