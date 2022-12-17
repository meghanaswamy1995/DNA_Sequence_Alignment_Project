from time import time
import psutil as p
import sys

def find_Memory():
    process = p.Process()
    memory_info = process.memory_info()
    totalMem = int(memory_info.rss / 1024)
    return totalMem

def create_sequence(seq, seq_arr):
    seq = seq.strip()
    newS1 = seq
    for index in seq_arr:
        index = int(index)
        first = newS1[0:index + 1]
        second = newS1[index + 1:]
        second = second.rstrip()
        newS1 = first + seq + second
        seq = newS1
    return seq


def sequence_validation(base_string,seq_arr,final_seq):
    length_seq_arr = len(seq_arr)
    length_base_string = len(base_string)-1
    length_final_seq = len(final_seq)
    if (2**length_seq_arr) * length_base_string == length_final_seq:
        return True
    return False

def basic_algorithm(seq1,seq2,gap_penalty): 
    m = len(seq1)
    n = len(seq2)
    dp = [[0]*(n + 1) for i in range(m + 1)]
    for i in range(n+1):
        dp[0][i] = i * gap_penalty
    for j in range(m+1):
        dp[j][0] = j * gap_penalty

    for i in range(1,m+1):
        for j in range(1,n+1):
                if seq1[i - 1] == seq2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    first = seq1[i-1]
                    second = seq2[j-1]
                    dp[i][j] = min(dp[i - 1][j - 1] + fetch_alpha(seq1[i - 1], seq2[j - 1]),
                                dp[i - 1][j] + gap_penalty,
                                dp[i][j - 1] + gap_penalty)
    return dp

def top_bottom_algorithm(dp,seq1,seq2,gap_penalty):
    m = len(seq1)
    n = len(seq2)
    seq_align1 = "" 
    seq_align2 = ""
    i = m
    j = n
    while not (i == 0 or j == 0):
        if i > 0 and j > 0 and seq1[i - 1] == seq2[j - 1]: 
            seq_align1 = seq1[i - 1] + seq_align1 
            seq_align2 = seq2[j - 1] + seq_align2 
            j -= 1
            i -= 1

        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + fetch_alpha(seq1[i - 1], seq2[j - 1]):
            seq_align1 = seq1[i - 1] + seq_align1 
            seq_align2 = seq2[j - 1] + seq_align2 
            j = j - 1
            i = i - 1
        
        else:
            if i > 0 and dp[i][j] == dp[i - 1][j] + gap_penalty:
                seq_align1 = seq1[i - 1] + seq_align1 
                seq_align2 = "_" + seq_align2
                i = i - 1

            elif j > 0 and dp[i][j] == dp[i][j - 1] + gap_penalty:
                seq_align1 = "_" + seq_align1 
                seq_align2 =  seq2[j - 1] + seq_align2  
                j = j - 1
        
        
    return dp[m][n], seq_align1, seq_align2


def fetch_alpha(l1, l2):
    letters = ['A', 'C', 'G', 'T']
    index1 = letters.index(l1)
    index2 = letters.index(l2)
    alpha_values = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
    return alpha_values[index1][index2]



if __name__ == '__main__':
    if len(sys.argv) <= 2:
        sys.exit("Please try again with proper input.")
    with open(sys.argv[1]) as f:
        seq_one = []
        seq_two = []
        string1 = f.readline()
        count = 1
        flag = 0
        gap_penalty = 30
        line = f.readline().strip()
        while line != "":
            if line.isalpha():
                string2 = line
                flag = 1
            elif flag == 1:
                seq_two.append(line)
                count += 1
            else:
                seq_one.append(line)
                count += 1
            line = f.readline().strip()
        f.close()
        sequence1 = create_sequence(string1, seq_one)
        sequence2 = create_sequence(string2, seq_two)

        if not (sequence_validation(string1,seq_one,sequence1)):
            print("Sequence not posible.")
        else:
            start = time()
            dp = basic_algorithm(sequence1,sequence2,gap_penalty)
            cost , seq1, seq2 = top_bottom_algorithm(dp,sequence1,sequence2, gap_penalty)
            end = time()
            time = (end - start) * 1000
            mem = find_Memory()
            resultFile = open(sys.argv[2], 'w+')
            resultFile.write(str(cost) + "\n")
            resultFile.write(seq1 + "\n")
            resultFile.write(seq2 + "\n")
            resultFile.write(str(time) + "\n")
            resultFile.write(str(mem) + "\n")
            resultFile.close()

