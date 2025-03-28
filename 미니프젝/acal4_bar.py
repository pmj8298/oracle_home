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
        p_values = [daily_counts[date].get('P', 0) for date in dates]
        l_values = [daily_counts[date].get('L', 0) for date in dates]
        a_values = [daily_counts[date].get('A', 0) for date in dates]

        # 막대 너비 설정
        bar_width = 0.3  

        # 날짜를 x축으로 설정
        x_indexes = range(len(dates))

        # 날짜 포맷 적용
        ax.set_xticks(x_indexes)
        ax.set_xticklabels([date.toString("MM-dd") for date in dates], rotation=45, ha='right', fontproperties=self.font_prop)

        # 막대 그래프
        ax.bar(x_indexes, p_values, width=bar_width, label='출석', color='darkblue', align='center')
        ax.bar(x_indexes, l_values, width=bar_width, label='지각', color='darkgreen', align='edge')
        ax.bar(x_indexes, a_values, width=bar_width, label='결석', color='darkred', align='edge')

        # y축 범위 조정 (최대값보다 +2 크게 설정)
        ax.set_ylim(0, max(max(p_values, default=0), max(l_values, default=0), max(a_values, default=0)) + 2)

        # y축 레이블 추가
        ax.set_ylabel("출결 인원 수", fontproperties=self.font_prop)

        # 제목 설정
        ax.set_title("날짜별 출결 현황", fontproperties=self.font_prop)

        # 범례 위치 조정
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # 그래프 다시 그리기
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
