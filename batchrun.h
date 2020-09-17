#! /bin/zsh

source ~/py37/bin/activate
for i in 1000 5000 10000 15000 20000
do
    for j in {1..10}
    do
        no_houses=$i
        python run.py -no_houses $no_houses -c 
    done
done

# if "-no_houses" in argv:
#    P.no_houses = int(argv[argv.index("-no_houses") + 1])
# if "-use_solver" in argv:
#    P.use_solver = False if "False" in argv[argv.index("-use_solver") + 1] else True
# if "-c" in argv:
#    P.load_data = "create"
# if "-r" in argv:
#    P.load_data = "read"
# if "-jobs_file" in argv:
#    P.jobs_file = argv[argv.index("-jobs_file") + 1]
# if "-ignore_globals" in argv:
#    P.use_globals = False
