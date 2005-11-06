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
(define (extract-requirements file-port)
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
(define (get-requirements file-names)
  (if (null? file-names) ; If the list of files name is null (empty)
      '()                ; return null.
      (let ((file-name (first file-names)))                  ; Otherwise, pick the first file
	(lset-union eq?                                      ; make an union of
		    (call-with-input-file  file-name         ; its requirements
		      extract-requirements)
		    (get-requirements (rest file-names)))))) ; and process tho other files.

;;; Make a regexp that will match any string of a list of strings.
(define (regexp-match-any strs)
  (string-append "(" (string-join strs "|") ")"))

;;; Having a list of .setup files, build the list of the libraries in them (the .so files).
(define (get-libraries file-names)
  (if (null? file-names)
      '()
      (let ((file-name (first file-names)))
	(lset-union eq?
		    (call-with-input-file file-name
		      (lambda (file-port)
			(rest (first (read file-port)))))
		    (get-libraries (rest file-names))))))

;; Get the list of files passed as arguments to this program.
(define files (rest (argv)))

;; Get a list of the extensions needed by those files.
(define extensions (map symbol->string (get-requirements files)))

;; Build the regexp to match any .setup file of the extensions we need.
(define ext-regexp (string-append (repository-path) "/" (regexp-match-any extensions) "\\.setup"))

;; Build the list of .setup files of the extensions we need.
(define setup-file-names (find-files (repository-path) ext-regexp))

;; Build the list of libraries we need.
(define libraries (get-libraries setup-file-names))

;; Print the list of libraries with no parenthesis and separated by spaces.
(display (string-join libraries " "))
