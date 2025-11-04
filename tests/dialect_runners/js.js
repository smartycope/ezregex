const fs = require('fs');

// Load JSON file
const regexs = JSON.parse(fs.readFileSync('data/compiled_regexs.json', 'utf8')).js;

// Custom assertion
function myassert(result, shouldBe, i, failing, e=null) {
    if (Boolean(result) !== shouldBe) {
        console.log(`
----------------------- TEST FAILED -----------------------
language       = \`js\`
pattern        = \`${i.ezregex}\`
compiled regex = \`${i.regex}\`
`);

        if (e) throw e;
        else console.log(`pattern should ${shouldBe ? '' : 'NOT '}match \`${failing.replace(/\n/g, '\\n')}\``);
        process.exit(1)
    }
}

function splitFlags(expr) {
    // This SHOULD work
    // const match = new RegExp("^/((?:(?:.|\n))+)/(\w+)?$", 'm').exec(expr);
    // return [match[1], match[2]];
    const parts = expr.split('/');
    const flags = parts[parts.length - 1];
    const regex = parts.slice(1, parts.length - 1).join('/');
    // console.log({parts, regex, flags});
    return [regex, flags];
}

// Run regex match tests
for (const i of regexs) {
    let re;
    try {
        re = new RegExp(...splitFlags(i.regex));
    } catch (e) {
        myassert(false, true, i, '', e);
    }
    for (const m of i.should) {
        myassert(re.test(m), true, i, m);
    }
    for (const m of i.shouldnt) {
        myassert(re.test(m), false, i, m);
    }
}

// Run replacement tests
const replacements = JSON.parse(fs.readFileSync('data/compiled_replacements.json', 'utf8')).js;

function replAssert(i, actual) {
    if (actual !== i.after) {
        console.log(`
----------------------- TEST FAILED -----------------------
language       = \`js\`
pattern        = \`${i.ezregex}\`
compiled regex = \`${i.regex}\`
replacement    = \`${i.ezrepl}\`
compiled repl  = \`${i.repl}\`
base           = \`${i.base}\`
after          = \`${i.after}\`

Replacing
    \`${i.ezregex}\` (\`${i.regex}\`)
with
    \`${i.ezrepl}\` (\`${i.repl}\`)
in
    \`${i.base}\`
yielded
    \`${actual}\`
not
    \`${i.after}\`
`);
        process.exit(1);
    }
}

for (const i of replacements) {
    try {
        const [regex, flags] = splitFlags(i.regex);
        const re = new RegExp(regex, flags + 'g');
        const actual = i.base.replaceAll(re, i.repl);
        replAssert(i, actual);
    } catch (e) {
        console.log(`Error replacing \`${i.ezregex}\` with \`${i.repl}\` in \`${i.base}\`: ${e.message}`);
        myassert(false, true, i, i.ezregex, e);
    }
}

console.log('pass');
