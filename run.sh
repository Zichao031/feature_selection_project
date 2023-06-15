pypy3 205proj.py > results/small/small_22_forward.txt << EOF
small22.txt
1
EOF


pypy3 205proj.py > results/small/small_22_backward.txt << EOF
small22.txt
2
EOF


pypy3 205proj.py > results/large/large_6_forward.txt << EOF
large6.txt
1
EOF

# Command to run your program and redirect output to output2.txt
pypy3 205proj.py > results/large/large_6_backward.txt << EOF
large6.txt
2
EOF