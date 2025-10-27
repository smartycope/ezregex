const fs = require('fs');

// Load JSON file
const regexs = JSON.parse(fs.readFileSync('data/compiled_regexs.json', 'utf8')).js;

// Custom assertion
function myassert(result, shouldBe, i, failing) {
    if (Boolean(result) !== shouldBe) {
        console.log(`
----------------------- TEST FAILED -----------------------
language       = \`js\`
pattern        = \`${i.ezregex}\`
compiled regex = \`${i.regex}\`
pattern should ${shouldBe ? '' : 'NOT '}match \`${failing.replace(/\n/g, '\\n')}\`
`);
        process.exit(1)
    }
}

// Run tests
for (const i of regexs) {
    const re = new RegExp(i.regex);
    for (const m of i.should) {
        myassert(re.test(m), true, i, m);
    }
    for (const m of i.shouldnt) {
        myassert(re.test(m), false, i, m);
    }
}

console.log('pass');
