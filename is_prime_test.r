is.prime <- function(x)
  vapply(x, function(y) sum(y / 1:y == y %/% 1:y), integer(1L)) == 2L
  
is.prime(c(13, 37, 43, 67, 73))

is.prime(c(29, 53, 59, 83, 89))

