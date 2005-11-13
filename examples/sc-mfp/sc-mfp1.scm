;;;; Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
;;;;
;;;; This file is part of scons-chicken.
;;;;
;;;; Scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
;;;; Scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
;;;; You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

(use sc-mfl)
(declare (uses sc-mfp2))

(define (sc-mfp1-proc)
  (display "Hello from sc-mfp1.scm of the scons-chicken multiple-file-program.")
  (newline)
  (sc-mfl1-proc))

(sc-mfp1-proc)
(sc-mfp2-proc)
