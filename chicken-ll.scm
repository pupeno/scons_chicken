;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(use srfi-1 srfi-13 posix)
(define rest cdr)

;;; Returns a list of all the names of the extensions being used by the source code that is get from the port file-port (to be used with call-with-input-file).
(define (extension-names file-port)
  (let process-form ((form (read file-port))) ; Read a form from form-port
    (if (eof-object? form)                    ; If it is eof
	'()                                   ; return the empty list.
	(if (or (eq? (first form) 'use)                  ; If it is 'use or 'require-extension
		(eq? (first form) 'require-extension))   ; (aka, list of extensions to use)
	    (lset-union eq?                              ; make the union
			(rest form)                      ; of the extension names and
			(process-form (read file-port))) ; the rest of the extensions on file.
	    (process-form (read file-port)))))) ; Otherwise keep processing.

;;; Find requirements returns a list of all the extensions that are required by the files (sources) passed as arguments.
(define (find-all-requirements file-names)
  (if (null? file-names) ; If the list of files name is null (empty)
      '()                ; return null.
      (let ((file-name (car file-names)))                         ; Otherwise, pick the first file
	(append (call-with-input-file  file-name extension-names) ; get the extensions
		(find-all-requirements (rest file-names))))))     ; and process tho other files.

;;;Make a regexp that will match any string of a list of strings.
(define (regexp-match-any strs)
  (string-append "(" (string-join strs "|") ")"))
 
;; Get the list of files passed as arguments to this program.
(define files (rest (argv)))

;; Get a list of the extensions needed by those files.
(define extensions (map symbol->string (find-all-requirements files)))

;; Build the regexp to match any .setup file of the extensions we need.
(define ext-regexp (string-append (repository-path) "/" (regexp-match-any extensions) "\\.setup"))

(display (find-files (repository-path) ext-regexp))
(newline)