#!/usr/bin/env Rscript

library(jsonlite)

regexs <- fromJSON("data/compiled_regexs.json")$r

myassert <- function(b, should_be, i, failing, e = NULL) {
  if (b != should_be) {
    cat("\n----------------------- TEST FAILED -----------------------\n")
    cat("language       = `R`\n")
    cat(sprintf("pattern        = `%s`\n", regexs[i, "ezregex"]))
    cat(sprintf("compiled regex = `%s`\n", regexs[i, "regex"]))
    cat(sprintf("pattern should %smatch `%s`\n", ifelse(should_be, "", "NOT "), gsub("\n", "\\\\n", failing)))
    if (!is.null(e)) {
      cat('Failed with an ERROR:')
      cat("error: ", e$message, "\n")
    }
    quit(status = 1)
  }
}

for (i in rownames(regexs)) {
  regex <- regexs[i, "regex"]
  for (m in regexs[i, "should"][[1]]) {
    tryCatch(
        myassert(grepl(regex, m, perl = FALSE), TRUE, i, m, NULL)
    , error = function(e) { myassert(FALSE, TRUE, i, m, e) })
  }
  for (m in regexs[i, "shouldnt"][[1]]) {
    tryCatch(
      myassert(grepl(regex, m, perl = FALSE), FALSE, i, m, NULL)
    , error = function(e) { myassert(TRUE, FALSE, i, m, e) })
  }
}

replacements <- fromJSON("data/compiled_replacements.json")$r

repl_assert <- function(i, actual) {
    if (actual != replacements[i, 'after']) {
        cat("\n----------------------- TEST FAILED -----------------------\n")
        cat("language       = `r`\n")
        cat(sprintf("pattern        = `%s`\n", replacements[i, "ezregex"]))
        cat(sprintf("compiled regex = `%s`\n", replacements[i, "regex"]))
        cat(sprintf("replacement    = `%s`\n", replacements[i, "ezrepl"]))
        cat(sprintf("compiled repl  = `%s`\n", replacements[i, "repl"]))
        cat(sprintf("base           = `%s`\n", replacements[i, "base"]))
        cat(sprintf("after          = `%s`\n", replacements[i, "after"]))
        cat("\n")
        cat("Replacing\n")
        cat(sprintf("    `%s`\n", replacements[i, "ezregex"]))
        cat("with")
        cat(sprintf("    `%s`\n", replacements[i, "repl"]))
        cat("in")
        cat(sprintf("    `%s`\n", replacements[i, "base"]))
        cat("yielded")
        cat(sprintf("    `%s`\n", actual))
        cat("not")
        cat(sprintf("    `%s`\n", replacements[i, "after"]))
        cat("\n")
        quit(status = 1)
    }
}

for (i in rownames(replacements)) {
    tryCatch(
        repl_assert(i, gsub(replacements[i, "regex"], replacements[i, "repl"], replacements[i, "base"]))
    # , error = function(e) { print(paste("Error replacing ", replacements[i, "ezregex"], " with ", replacements[i, "repl"], " in ", replacements[i, "base"]: str(e))) })
    , error = function(e) { repl_assert(i, "") })
}

cat("pass\n")
