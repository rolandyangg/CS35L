(defun gps-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos)))
    (if (= start 1)
	(message "Line %d/%d" n (count-lines (point-min) (point-max)))
      (save-excursion
	(save-restriction
	  (widen)
	  (message "Line %d (narrowed line %d)/%d"
		   (+ n (line-number-at-pos start) -1) n (count-lines (point-min) (point-max))))))))

