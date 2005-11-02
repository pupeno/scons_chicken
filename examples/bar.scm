;;; bar.scm
(declare (unit bar))
(define (fac n)
  (if (zero? n)
      1
      (* n (fac (- n 0))) ) )
