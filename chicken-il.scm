;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(use srfi-1 srfi-13 posix)
(define rest cdr)

(define (get-includes filename)
  (call-with-input-file filename
    (lambda (file-port)
      (let process-form ((form (read file-port))) ; Read a form from form-port
        (if (eof-object? form)                    ; If it is eof
            '()                                   ; return the empty list.
            (if (eq? (first form) 'include)                  ; If it is 'include
                (lset-union eq?                              ; make the union
                            (rest form)                      ; of the include and
                            (process-form (read file-port))) ; the rest of the includes on file.
                (process-form (read file-port)))))))) ; Otherwise keep processing.

;; Get the list of files passed as arguments to this program.
(define file (first (rest (argv))))

;; Get a list of the extensions needed by those files.
(define includes (get-includes file))

;; Print the list of includes with no parenthesis and separated by spaces.
(display (string-join includes " "))
(newline)
