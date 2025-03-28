import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
import cx_Oracle as oci
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
import matplotlib.dates as mdates  # 날짜 포맷용 라이브러리
import numpy as np

# 데이터베이스 연결 정보
sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'


class AttendanceGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        font_path = "C:/Windows/Fonts/malgun.ttf"
        self.font_prop = self.set_korean_font(font_path)

    def set_korean_font(self, font_path):
        try:
            font = fm.FontProperties(fname=font_path)
            return font
        except Exception as e:
            print("폰트 로드 오류:", e)
            return None


    def update_graph(self, daily_counts):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # 날짜 정렬
        dates = sorted(daily_counts.keys())

        # ✅ 출석 데이터를 출석일수(0, 0.5, 1)로 변환
        attendance_values = [daily_counts[date].get('P', 0) for date in dates]
        attendance_values = [1 if v >= 1 else 0.5 if v > 0 else 0 for v in attendance_values]  # 변환 로직

        # 🔹 x축 인덱스 생성
        x_indexes = range(len(dates))

        # ✅ x축 날짜 포맷 적용
        ax.set_xticks(x_indexes)
        ax.set_xticklabels([date.toString("MM-dd") for date in dates], 
                        rotation=45, ha='right', fontproperties=self.font_prop)

        # ✅ 출석 상태에 따라 마커 변경
        markers = ['o' if v == 1 else '△' if v == 0.5 else 'x' for v in attendance_values]

        # ✅ 그래프 플롯
             # ✅ 그래프 플롯 (마커 중앙 정렬)
        for i, (x, y, marker) in enumerate(zip(x_indexes, attendance_values, markers)):
            # 기존 scatter는 보조 역할로 유지 (크기 조절)
            ax.scatter(x, y, marker=marker, color='darkblue', s=100, label="출석" if i == 0 else "")
            
            # 마커를 중심에 정확히 맞추기 위해 텍스트 사용 (위치 조정)
            offset_y = 0.02  # y축 미세 조정 (위로 약간 올림)
            ax.text(x, y - offset_y, marker, color='darkblue', fontproperties=self.font_prop,
                    ha='center', va='center', fontsize=12)  # ha, va로 중심 정렬



        # ✅ y축 범위 0~1 설정 및 레이블 적용
        ax.set_yticks([0, 0.5, 1])
        ax.set_yticklabels(['X', '△', 'O'], fontproperties=self.font_prop)

        # ✅ y축 레이블 추가
        ax.set_ylabel("출석 일수", fontproperties=self.font_prop)

        # ✅ 그래프 제목 설정
        ax.set_title("날짜별 출석 현황", fontproperties=self.font_prop)

        # ✅ 그래프 다시 그리기
        self.canvas.draw()





class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.symbols = {}
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.parent = parent
        self.load_attendance_data()

    def load_attendance_data(self):
        """ 데이터베이스에서 출결 정보를 가져와 저장 """
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            query = '''
                SELECT ATD_DATE, STATUS 
                FROM ATTENDANCE.ATD 
                WHERE S_NO = 1 
                AND EXTRACT(MONTH FROM ATD_DATE) = 2
            '''
            cursor.execute(query)
            rows = cursor.fetchall()

            status_map = {'P': 'O', 'L': '△', 'A': 'X'}
            daily_counts = {}

            for date, status in rows:
                qdate = QDate(date.year, date.month, date.day)
                if qdate not in daily_counts:
                    daily_counts[qdate] = {'P': 0, 'L': 0, 'A': 0}
                daily_counts[qdate][status] += 1
                self.symbols[qdate] = status_map.get(status, "")

            print("출결 데이터 로드 완료:", daily_counts)

            self.parent.update_attendance_labels(daily_counts)
            self.parent.graph_widget.update_graph(daily_counts)

        except Exception as e:
            print("데이터베이스 오류:", e)

        finally:
            cursor.close()
            conn.close()

    def paintCell(self, painter, rect, date):
        """ 달력에 출결 상태를 표시 """
        super().paintCell(painter, rect, date)

        if date in self.symbols:
            symbol = self.symbols[date]
            color_map = {'O': "blue", '△': "green", 'X': "red"}

            # 기호 색상 설정
            painter.setPen(QColor(color_map.get(symbol, "black")))

            # 기호 표시
            font = QFont("Arial", 12, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect.adjusted(rect.width() // 3, 0, 0, 0), Qt.AlignLeft, symbol)


class AttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./미니프젝/출석관리,통계3.ui', self)

        self.graph_widget = AttendanceGraph(self)

        vertical_layout = self.findChild(QVBoxLayout, "verticalLayout")
        if vertical_layout:
            vertical_layout.addWidget(self.graph_widget)
            vertical_layout.addStretch(1)

        self.graph_widget.setMinimumHeight(50)
        self.graph_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        old_calendar = self.findChild(QCalendarWidget, "calendarWidget")
        if old_calendar:
            self.custom_calendar = CustomCalendar(self)
            self.custom_calendar.setGeometry(old_calendar.geometry())
            self.custom_calendar.setObjectName("calendarWidget")
            layout = old_calendar.parentWidget().layout()
            if layout:
                layout.replaceWidget(old_calendar, self.custom_calendar)
            old_calendar.deleteLater()

        text_browser = self.findChild(QTextBrowser, "textBrowser")
        if text_browser:
            container = QWidget(text_browser)
            text_browser.setViewport(container)
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(self.graph_widget)

    def update_attendance_labels(self, daily_counts):
        """ 그래프를 업데이트하는 메서드 """
        print(f"출결 카운트 업데이트: {daily_counts}")
        if hasattr(self, 'graph_widget') and self.graph_widget:
            self.graph_widget.update_graph(daily_counts)
        else:
            print("graph_widget이 초기화되지 않았습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())
