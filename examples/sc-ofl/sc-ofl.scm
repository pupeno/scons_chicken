;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; Scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; Scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(define-extension sc-ofl)
(declare (export sc-ofl-proc))

;;; An example of a procedure defined in a library/extension that will be called by other programs and extensions.
;;; It is called sc-ofl-proc to avoid confusion/overlaping with the extension itself.
(define (sc-ofl-proc)
  (display "Hello from sc-ofl, the scons-chicken one-file-library.")
  (newline))
