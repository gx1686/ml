from numpy import  *

a = [
    [1,2,3],
    [11,22,33],
    [111,222,333]
]

b = mat(a)
c = b[:,1]

d = b[0,:]
print c,d

print b

c = [1,2]
print tile(c,(1,2))


print 'test min & max'



a = [
    [1,2,3],
    [1.1,2.2,33],
    [111,222,333]
]
myMat = mat(a)
print myMat.min(0)
print myMat.max(0)


print '-------------'

print zeros(shape(myMat))




