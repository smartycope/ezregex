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
  for (m in regexs[i, "should"][[1]]) {
    tryCatch(
      myassert(grepl(regexs[i, "regex"], m, perl = FALSE), TRUE, i, m, NULL)
    , error = function(e) { myassert(FALSE, TRUE, i, m, e) })
  }
  for (m in regexs[i, "shouldnt"][[1]]) {
    tryCatch(
      myassert(grepl(regexs[i, "regex"], m, perl = FALSE), FALSE, i, m, NULL)
    , error = function(e) { myassert(TRUE, FALSE, i, m, e) })
  }
}


cat("pass\n")
