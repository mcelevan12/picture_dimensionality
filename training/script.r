# load aclove from the slp library
library(catlearn)
pca.dir = "~/Documents/picture_dimensionality/training/training_data"
modeling.dir = "~/Documents/picture_dimensionality/training/modeling"
conditions = c("near", "far", "rand")
training.files = c("PCA01.csv", "PCA02.csv", "PCA03.csv", "PCA04.csv", "PCA05.csv", "PCA06.csv", "PCA07.csv", "PCA08.csv", "PCA09.csv", "PCA10.csv", "PCA11.csv", "PCA12.csv")
output.files = c("DIM01.csv", "DIM02.csv", "DIM03.csv", "DIM04.csv", "DIM05.csv", "DIM06.csv", "DIM07.csv", "DIM08.csv", "DIM09.csv", "DIM10.csv", "DIM11.csv", "DIM12.csv")
c = c(seq(0.5, 4, by=0.25), seq(4.5, 7, by=0.5))
lw = c(0.01, 0.025, seq(.05, 0.4, by=.05))
la = c(0, lw)
phi = seq(0, 10, by=0.25)
all.params = expand.grid(c = c, lw = lw, la = la, phi = phi)
colskip = 3
# find out write/mem limits to find what this should be
row.buffer = 10000
some.params = all.params #[sample(nrow(all.params), row.buffer*2.5),] 
# just had that here for testing purposes so I didnt run everyhting on my laptop

total = nrow(some.params) * 12 * 3
iter = 0
start = Sys.time()
previous.iteration = Sys.time()
#for dim in dims and for condition in condition
for(dims in 1:12) {
  for(condition in 1:3) {
    out.file = paste(modeling.dir, conditions[condition], output.files[dims], sep = "/")
    tr = data.matrix(read.csv(paste(pca.dir, conditions[condition], training.files[dims], sep = "/")))
    probs = array(NA, c(row.buffer, 2, 216))
    dimnames(probs)[[3]] = paste("o", 1:216, sep = "")
    alphas = array(NA, c(row.buffer, dims))
    colnames(alphas) = paste(rep("a", dims), 1:dims, sep = "")
    ws = array(NA, c(row.buffer, 2, 18))
    dimnames(ws)[[3]] = paste(rep("w", 18	), 1:18, sep = "")
    sts = data.frame(array(-1, c(row.buffer, 4)))
    colnames(sts) =  c("c", "phi", "lw", "la")
    cols.needed = TRUE
    h = t(tr[0:18, 4:(4+dims-1)])
    #looks all ugly and gross but needs to be this way to not have a billion off by one errors
    for(i in 1:nrow(some.params)) {
      #0indexingmasterrace would make this shit soo much easier
      curr.row = (i - 1)%%row.buffer + 1
      sts$c[curr.row] = some.params$c[i]
      sts$phi[curr.row] = some.params$phi[i]
      sts$lw[curr.row] = some.params$lw[i]
      sts$la[curr.row] = some.params$la[i]
      st = list(
          c = some.params$c[i],
          phi = some.params$phi[i],
          lw = some.params$lw[i],
          la = some.params$la[i],
          r = 1,
          q = 1,
          w = matrix(0, 2, 18),
          h = h,
          alpha = rep(1, dims), 
          colskip = 3)
      # TODO permute tr and fix NA's here
      #also probs needs to be fixed if were permuting tr's
      out = slpALCOVE(st, tr)
      probs[curr.row,,] = out$prob
      alphas[curr.row,] = out$alpha
      ws[curr.row,,] = out$w
      if(i %% row.buffer == 0) {
        #for some reason write.table doesent add the empty col name need for the row names :/ can jsut do it manually
        write.table(cbind(sts, alphas, ws, probs), out.file, sep = ",", append = !cols.needed, col.names = cols.needed, row.names = (i - row.buffer + 1):i)
        cols.needed = FALSE
      } 
      iter = iter + 1
      if(iter %% (row.buffer) == 0) {
        print(paste("iteration:", iter, "out of", total))
        print(paste("total time:", Sys.time() - start))
        print(paste("this iteration:", Sys.time() - previous.iteration))
        previous.iteration = Sys.time()
      }
    }
    #write last rows
    if(i %% row.buffer != 0) {
      write.table(cbind(sts, alphas, ws, probs)[1:(i %% row.buffer),], out.file, sep = ",", append = !cols.needed, col.names = cols.needed, row.names = (i - i %% row.buffer + 1):i)
    }
  }
}

