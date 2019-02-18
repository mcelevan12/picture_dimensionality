st = list(c = 7,
          phi = 6.5,
          lw = 0.35,
          la = 0,
          r = 1,
          q = 1, 
          w = matrix(0, 2, 18),
          h = t(tr[0:18, 4:5]),
          alpha = c(1, 1),
          colskip = 3
)
slpALCOVE(st, tr)
