;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; Scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; Scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(use sc-lapl)

;;; An example of a procedure defined on a program that uses a procedure from an extension.
;;; It is named sc-lapp-proc to avoid conflict/confusion with the program itself.
(define (sc-lapp-proc)
  (display "Hello from sc-lapp, the scons-chicken library-and-program program.")
  (newline)
  (sc-lapl-proc))

(sc-lapp-proc)
