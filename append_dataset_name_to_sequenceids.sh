# cd results_from_vsc/blast_results/test
# LST=(*)
# for f in ${LST[*]};
# do
# string="$(cut -d_ -f4 <<< "$(cut -d. -f1 <<< $f)")_"
# sed -i -e "s/^/${string}/" $f
# done

# cd results_from_vsc/blast_results/test
# LST=(*)
# for f in ${LST[*]};
# do
# sed -i '1iqaccver,saccver,evalue,pident,length,qlen,qstart,qend,sstart,send,sseq,qseq' $f
# done
# echo "done"