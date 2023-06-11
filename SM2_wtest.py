from time import perf_counter
from SM2 import SM2
from config_parser import config_parser


def main():
    conp=config_parser()
    p=conp.config['p']
    a=conp.config['a']
    b=conp.config['b']
    G=conp.config['G']
    pb=conp.config['pb']
    k=conp.config['k']
    N = conp.config['N']
    floor = conp.config['floor']
    ceil = conp.config['ceil']
    sm2 = SM2(a, b, p, G)
    print(f"#当前参数为：\np = %s\na = %s\nb = %s\nk = %s"%(hex(p), hex(a), hex(b), hex(k)))
    print("G = (%s, %s)"%tuple(map(hex,G)))
    print("P_b = (%s, %s)"%tuple(map(hex,pb)))
    print()
    for w in range(floor,ceil):
        print(f"滑动窗口大小为：%d"%w)
        print(f"#测试%d次计算基点的倍点，结果为："%N)
        start = perf_counter()
        for i in range(N):
            tmp = sm2.mul(k, G)
        end = perf_counter()
        norm=end-start
        print(f"优化前运行时间：%lf秒"%norm)
        sm2.pre_process(G, w)#预处理
        start = perf_counter()
        for i in range(N):
            tmp = sm2.mul_optimizer(k, G, w, 1)#使用优化后的乘法
        end = perf_counter()
        optim=end-start
        print(f"优化后运行时间：%lf秒"%optim)
        print(f"优化率：%lf%%"%(optim*100/norm))
        print(f"#测试%d次计算私钥的倍点，结果为："%N)
        start = perf_counter()
        for i in range(N):
            tmp = sm2.mul(k, pb)
        end = perf_counter()
        norm = end - start
        print(f"优化前运行时间：%lf秒"%(end - start))
        start = perf_counter()
        for i in range(N):
            tmp = sm2.mul_optimizer(k, pb, w, 0)
        end = perf_counter()
        optim = end - start
        print(f"优化后运行时间：%lf秒"%(end - start))
        print(f"优化率：%lf%%" % (optim * 100 / norm))
        print()
if __name__ == "__main__":
    main()