import matplotlib.pyplot as plt
import os
import csv
def test_script(root):
    root = root + '\\'
    file_list = os.listdir(root)
    for file in file_list:
        with open(root + file, encoding='utf-8') as f:
            reader = csv.reader(f)
            record = []
            x_labels = []
            for r in reader:
                record.append(float(r[0]))  # Assuming r[0] contains numerical data
                x_labels.append(reader.line_num)  # Using line number as x-axis
            print(record[0], record[len(record) - 1])
            interval = (record[len(record) - 1] - record[0]) / 2000
            print(interval)
            cur_Least_Line = [0.0 for _ in range(len(record))]
            cur_Least_Line[0] = record[0] + interval
            for i in range(len(record)):
                if i > 0:
                    cur_Least_Line[i] = cur_Least_Line[i - 1] + interval
            plt.figure(0)
            plt.plot(x_labels, record)
            plt.plot(x_labels, cur_Least_Line,color='r')
            plt.xlabel('Data Index')
            plt.ylabel('TimeStamp')
            plt.title(f'File: {file}')
            plt.grid(True)
            plt.show()
if __name__ == '__main__':
    test_script("Data")
