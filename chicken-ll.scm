;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(declare (uses srfi-1))

;;; Returns a list of all the names of the extensions being used by the source code that is get from the port file-port (to be used with call-with-input-file).
(define (extension-names file-port)
  (let process-form ((form (read file-port)))
    (if (eof-object? form)
	'()
	(if (and (eqv? (car form) 'declare)
		 (eqv? (caadr form) 'uses))
	    (append (cdadr form) (process-form (read file-port)))
	    (process-form (read file-port))))))

;;; Find requirements returns a list of all the extensions that are required by the files (sources) passed as arguments.
(define (find-all-requirements file-names)
  (if (null? file-names) 
      '()
      (let ((file-name (car file-names)))
	(append (call-with-input-file file-name extension-names)
		(find-all-requirements (cdr file-names))))))

;;; All parameters are files.
(define files (cdr (argv)))

;;; Find the requirements of all files.
(display (find-all-requirements files))
(newline)