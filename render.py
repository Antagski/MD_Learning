import time
import os
import PySide6.QtWidgets

os.environ['OVITO_GUI_MODE'] = '1'  # Request a session with OpenGL support
app = PySide6.QtWidgets.QApplication()


from ovito.io import import_file
from ovito.vis import Viewport, TachyonRenderer, OpenGLRenderer, AnariRenderer
from ovito.modifiers import CommonNeighborAnalysisModifier, SliceModifier




def render_anim(vp, filename='video_test.mp4', size=(800, 1200), fps=60, background=(1, 1, 1),
                   every_nth=2, range=(0, 60), renderer=OpenGLRenderer(antialiasing_level=1)):
    vp.render_anim(filename=filename, size=size, fps=fps, background=background,
                   every_nth=every_nth, range=range, renderer=renderer)
# OpenGLRenderer(antialiasing_level=1) 抗锯齿级别：1没有，n为n倍超采样
# size决定清晰度，size越大，清晰度越高，如果renderer=TachyonRenderer()表示用cpu渲染，会慢很多，但好像更精致


def render_image(vp, filename='image.png', size=(3000, 3000), frame=0, background=(1, 1, 1),
                renderer=OpenGLRenderer(antialiasing_level=4)):
    vp.render_image(filename=filename, size=size, frame=frame, background=background,
                    renderer=renderer)


def read_file(PATH):
    pipeline = import_file(PATH)  # 轨迹文件
    # D:/Atomsk/Model/合金拉伸/CoNiCr/Outputs/75_150_600/CoCrNiTension.xyz

    pipeline.add_to_scene()
    # slice = SliceModifier(enabled=True, distance=120.0, normal=(0, 0, 1), )
    # pipeline.modifiers.append(slice)
    # 先切割，再分析
    common = CommonNeighborAnalysisModifier()
    pipeline.modifiers.append(common)

    vp = Viewport(type=Viewport.Type.Ortho, camera_dir=(1, 0, 0), )  # camera_dir = (0, 0, 1)表示从Z轴方向看去
    vp.zoom_all()
    return vp

if __name__ == "__main__":

    vp = read_file()

    start_time = time.time()
    render_image(vp)
    end_time = time.time()
    print(f"Cost time: {end_time - start_time}")
