pypy3 205proj.py > results/small/small_22_forward.txt << EOF
data/small22.txt
1
EOF


pypy3 205proj.py > results/small/small_22_backward.txt << EOF
data/small22.txt
2
EOF


pypy3 205proj.py > results/large/large_6_forward.txt << EOF
data/large6.txt
1
EOF

# Command to run your program and redirect output to output2.txt
pypy3 205proj.py > results/large/large_6_backward.txt << EOF
data/large6.txt
2
EOF