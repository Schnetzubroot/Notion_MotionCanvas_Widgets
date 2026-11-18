from sympy import *
t,x,w,a,b,c,R,k,A,v0,d,q0,L,al,u=symbols('t x omega a b c R k A v_0 delta q_0 L alpha u',positive=True)
def chk(name,expr): 
    r=simplify(expr); print(name, 'OK' if r==0 else f'FAIL {r}')
# A1
chk('A1', diff(sin(w*t)**2,t)-w*sin(2*w*t))
# A2 d/dx ln tan(x/2) = 1/sin x
chk('A2', diff(log(tan(x/2)),x)-1/sin(x))
# A3
chk('A3a', diff(atan(x/a),x)-a/(a**2+x**2))
phi=atan((R*sin(w*t))/(R*cos(w*t))); chk('A3b', diff(phi,t)-w)
# A4 rho dot
X,Y=Function('x')(t),Function('y')(t)
chk('A4', diff(sqrt(X**2+Y**2),t)-(X*X.diff(t)+Y*Y.diff(t))/sqrt(X**2+Y**2))
# A5
xx=exp(-d*t)*cos(w*t)
print('A5 xdot', simplify(diff(xx,t)), ' xdd', simplify(diff(xx,t,2)))
chk('A5', diff(xx,t,2)+2*d*diff(xx,t)+(d**2+w**2)*xx)
# A6: x=A sin^2(kt), xdot = A k sin 2kt; compare with v0 sin(v0 t / b): k=v0/(2b), A=2b
bb=symbols('b',positive=True)
chk('A6', diff((2*bb)*sin(v0/(2*bb)*t)**2,t)-v0*sin(v0*t/bb))
# A7 polar
p=Function('phi')(t); r=Function('rho')(t)
er=Matrix([cos(p),sin(p),0]); ep=Matrix([-sin(p),cos(p),0])
chk('A7a', (er.diff(t)-p.diff(t)*ep).norm()**2)
chk('A7b', (ep.diff(t)+p.diff(t)*er).norm()**2)
rv=r*er; acc=rv.diff(t,2)
chk('A7c', (acc - ((r.diff(t,2)-r*p.diff(t)**2)*er+(2*r.diff(t)*p.diff(t)+r*p.diff(t,2))*ep)).norm()**2)
# B
chk('B1', integrate(sin(w*t)**2,(t,0,2*pi/w))-pi/w)
print('B2', integrate(sin(x)*cos(x),x))
chk('B3a', diff(-exp(-x**2)/2,x)-x*exp(-x**2))
chk('B3b', diff(sqrt(1+t**2),t)-t/sqrt(1+t**2))
chk('B3c', diff(-log(cos(x)),x)-tan(x))
chk('B4a', diff(x*sin(x)+cos(x),x)-x*cos(x))
chk('B4b', diff((x-1)*exp(x),x)-x*exp(x))
chk('B4c', diff(x*log(x)-x,x)-log(x))
chk('B4d', diff(exp(t)*(sin(t)-cos(t))/2,t)-exp(t)*sin(t))
for name,q,RR,xs in [('B5a',q0*sin(pi*x/L),2*q0*L/pi,L/2),('B5b',q0*x/L,q0*L/2,2*L/3),('B5c',q0*(x/L)**2,q0*L/3,3*L/4)]:
    Rr=integrate(q,(x,0,L)); chk(name+'R',Rr-RR); chk(name+'x',integrate(x*q,(x,0,L))/Rr-xs)
# B6 helix
rh=Matrix([R*cos(w*t),R*sin(w*t),c*t]); sp=sqrt(rh.diff(t).dot(rh.diff(t)))
chk('B6', sp-sqrt(R**2*w**2+c**2)); print('B6 s(T)=', simplify(integrate(simplify(sp),(t,0,2*pi/w))))
# B7
a0=symbols('a_0',positive=True)
vv=integrate(a0*cos(w*u),(u,0,t)); xv=integrate(vv.subs(t,u),(u,0,t))
chk('B7v',vv-a0/w*sin(w*t)); chk('B7x',xv-a0/w**2*(1-cos(w*t)))
chk('B8a', integrate(sin(x)**2,(x,0,pi/2))-pi/4); chk('B8b', integrate(x*sin(x),(x,0,pi))-pi)
chk('B9a', diff(atan(x/a)/a,x)-1/(a**2+x**2)); 
# C
av=Matrix([2,-1,2]); bv=Matrix([1,2,2])
print('C1', av.norm(), bv.norm(), av.dot(bv), av.cross(bv).T, av.cross(bv).norm(), av.dot(av.cross(bv)), bv.dot(av.cross(bv)))
ba=av.dot(bv)/av.dot(av)*av; print('C2', av.dot(bv)/av.norm(), ba.T, (bv-ba).T, (bv-ba).dot(av))
ex,ey,ez=eye(3)[:,0],eye(3)[:,1],eye(3)[:,2]
print('C3', ex.cross(ex.cross(ey)).T, (ex.cross(ex)).cross(ey).T)
lam=symbols('lambda'); M=Matrix([[1,2,3],[2,lam,1],[1,1,-1]]); print('C4 det', expand(M.det()), solve(M.det(),lam), M.det().subs(lam,0))
MN=Matrix([3,4,0]); vM=Matrix([2,0,0]); om=symbols('omega_z')
vN=vM+Matrix([0,0,om]).cross(MN); print('C5', vN.T, solve(vN[0],om), vN.subs(om,Rational(1,2)).T, vM.dot(MN))
omv=Matrix([0,0,2]); vB=Matrix([1,0,0]); print('C6', (vB+omv.cross(Matrix([1,1,0]))).T, (vB+omv.cross(Matrix([0,Rational(1,2),0]))).T)
vB2=Matrix([1,2,3]); vM2=vB2+omv.cross(Matrix([1,0,0])); print('C7', vM2.T, vM2.dot(omv), vB2.dot(omv))
F=Matrix([0,0,-10]); OA=Matrix([2,1,0]); MO=OA.cross(F); MB=MO+F.cross(Matrix([0,1,0])); print('C8', MO.T, MB.T, Matrix([2,0,0]).cross(F).T)
print('C9', Matrix([3,-1,0]).dot(Matrix([-1,2,0])))
# D1
ph=al*t**2/2; r1=R*Matrix([cos(ph),sin(ph)]); v1=r1.diff(t); a1=v1.diff(t)
print('D1 |v|', simplify(sqrt(v1.dot(v1))), ' a', simplify(a1.T)); 
et=v1/(R*al*t); en=-Matrix([cos(ph),sin(ph)])
print('D1 at,an', simplify(a1.dot(et)), simplify(a1.dot(en)))
# D2
r2=Matrix([a*cos(w*t),b*sin(w*t)]); v2=r2.diff(t); a2=v2.diff(t)
chk('D2a', (a2+w**2*r2).norm()**2); print('D2 r.v', factor(simplify(r2.dot(v2))), ' |v|^2', simplify(v2.dot(v2)))
# D3
xd=-2*a*k*sin(k*t); T=2*pi/k
print('D3 mean v', integrate(xd,(t,0,T))/T, ' mean speed', simplify(4*integrate(-xd,(t,0,pi/k))/2/T))
# D4 cycloid
rc=Matrix([R*(w*t-sin(w*t)), R*(1-cos(w*t))]); vc=rc.diff(t)
sp2=simplify(vc.dot(vc)); chk('D4a', sp2-4*R**2*w**2*sin(w*t/2)**2)
print('D4 s', integrate(2*R*w*sin(w*t/2),(t,0,2*pi/w)))
CP=rc-Matrix([R*w*t,0]); chk('D4b', simplify(CP.dot(CP))-4*R**2*sin(w*t/2)**2)
vcross=Matrix([w*CP[1], -w*CP[0]]) # omega=(0,0,-w) for rolling to +x: (-w ez) x (cx,cy) = (w cy, -w cx)
chk('D4c', (vcross-vc).norm()**2)
# D5 spiral
r5=Matrix([c*t*cos(w*t), c*t*sin(w*t)]); v5=r5.diff(t); a5=v5.diff(t)
er5=Matrix([cos(w*t),sin(w*t)]); ep5=Matrix([-sin(w*t),cos(w*t)])
print('D5 v', simplify(v5.dot(er5)), simplify(v5.dot(ep5)), ' a', simplify(a5.dot(er5)), simplify(a5.dot(ep5)), ' |v|', simplify(sqrt(v5.dot(v5))))
# E
chk('E1', diff(sin(x)*cos(x),x)-cos(2*x)); chk('E2', integrate(cos(x)**2,(x,0,pi))-pi/2)
