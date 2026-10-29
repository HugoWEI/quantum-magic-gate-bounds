"""Independent symbolic validation: python -m src.symbolic_verify."""
from sympy import symbols, sqrt, expand, factor, groebner

c, q, u, v = symbols("c q u v", real=True)
ps = {("I","I"):1,("I","Z"):c,("Z","I"):c,("Z","Z"):1,
      ("X","X"):q*u,("X","Y"):q*v,
      ("Y","X"):q*v,("Y","Y"):-q*u}
labels="IXYZ"

def raw_moment():
    return expand(sum(x**4 for x in ps.values()))

def rotated_moment(axis):
    pair={"Z":("X","Y"),"X":("Y","Z"),"Y":("Z","X")}[axis]
    s=0
    for other in labels:
        for first in labels:
            if first not in pair:
                s+=ps.get((first,other),0)**4
        x=ps.get((pair[0],other),0)
        y=ps.get((pair[1],other),0)
        s+=((x+y)/sqrt(2))**4+((x-y)/sqrt(2))**4
    return expand(s)

def remainder(a):
    ideal=groebner([c*c+q*q-1,u*u+v*v-1],c,u,q,v)
    return factor(ideal.reduce(expand(a))[1])

def verify():
    original=raw_moment()
    z=rotated_moment("Z")
    x=rotated_moment("X")
    base=4-4*q*q+4*q**4
    s=4*u*u*v*v
    assert remainder(original-(base-q**4*s))==0
    assert remainder(z-(base-q**4*(1-s)))==0
    assert expand(4*x-3*original)==0
    print("PASS: R_in = 4-4q^2+4q^4-q^4 s")
    print("PASS: R_after_Z = 4-4q^2+3q^4+q^4 s")
    print("PASS: 4 R_after_X = 3 R_in; q=sin(2theta), s=sin^2(2phi)")

if __name__=="__main__":
    verify()
