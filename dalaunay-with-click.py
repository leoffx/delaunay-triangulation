import matplotlib.pyplot as plt
import numpy as np

point_num = 10  #número de pontos aleatórios

points = np.random.rand(point_num, 2)  #inicializa pontos aleatórios
ien = []  #IEN
eql = []  #equilateralidade do triangulo

fig, ax = plt.subplots()


def CCW(
        p, q, r
):  #usa o produto vetorial pra dizer se o ponto R está a sentido anti horario dos outros dois
    return (q[1] - p[1]) * (r[0] - p[0]) < (r[1] - p[1]) * (q[0] - p[0])


def delaunay(
        a, b, c, d
):  #determina se o quarto ponto está dentro da circunferencia // precisa que a,b,c esteja em ordem anti horaria
    det = np.linalg.det(
        [[a[0] - d[0], a[1] - d[1], (a[0] - d[0])**2 + (a[1] - d[1])**2],
         [b[0] - d[0], b[1] - d[1], (b[0] - d[0])**2 + (b[1] - d[1])**2],
         [c[0] - d[0], c[1] - d[1], (c[0] - d[0])**2 + (c[1] - d[1])**2]])
    return det > 0


def triangulate(points):
    global point_num, fig, ax

    ien = []  #IEN
    eql = []  #equilateralidade do triangulo
    for i in range(point_num):  #fixa primeiro ponto da triangulaçao
        p = points[i, :]
        for j in range(i, point_num):  #fixa segundo ponto
            q = points[j, :]
            for k in range(i, point_num):  #fixa terceiro ponto
                r = points[k, :]
                z = 0
                if CCW(p, q, r):
                    for l in range(
                            point_num
                    ):  #confere se os outros pontos estão fora da triangulação
                        s = points[l, :]
                        if delaunay(
                                p, q, r, s
                        ):  #se houver algum ponto dentro da circunferencia, não plotar
                            z += 1
                            break
                    if z == 0:  #se nenhum outro ponto fica dentro da circunferência que contém os 3 (p,q,r)
                        plt.plot([p[0], q[0]], [p[1], q[1]],
                                 'r-',
                                 lineWidth=.5)  #triangula
                        plt.plot([r[0], q[0]], [r[1], q[1]],
                                 'r-',
                                 lineWidth=.5)
                        plt.plot([p[0], r[0]], [p[1], r[1]],
                                 'r-',
                                 lineWidth=.5)

                        pq = np.linalg.norm(
                            p - q)  #medição do grau de equilateralidade
                        rq = np.linalg.norm(r - q)
                        pr = np.linalg.norm(p - r)
                        perim = (pq + rq + pr) / 2
                        sqrtArea = (perim * (perim - pq) * (perim - rq) *
                                    (perim - pr))**.25
                        eql = (3**.75 * sqrtArea) / perim

                        ien = np.append(ien, [i, j, k, eql])  #monta IEN + grau
    #numera os pontos no grafico
    for i, txt in enumerate(range(point_num)):
        ax.annotate(txt, (points[i, 0], points[i, 1]))

    ien = np.reshape(ien, (-1, 4))

    qualityAvg = np.mean(ien[:, 3])
    print(
        ien.shape, ien,
        '\n Grau de equilateralidade médio dos triângulos: ' + str(qualityAvg))


triangulate(points)


def onclick(event):
    global points, point_num
    fig.clf()  #limpa canvas

    point_num += 1

    click = np.array([[event.xdata,
                       event.ydata]])  #coordenada do mouse ao clickar

    points = np.concatenate((points,
                             click))  #adiciona coordenada do click aos pontos

    triangulate(points)  #desenha triangulaçao

    plt.plot(points[:, 0], points[:, 1], 'b.')  #desenha os pontos

    fig.canvas.draw()


cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.plot(points[:, 0], points[:, 1], '.')
plt.show()
