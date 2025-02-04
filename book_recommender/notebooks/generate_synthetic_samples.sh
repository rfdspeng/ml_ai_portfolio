# for i in {1..20}; do
#     python3 generate_synthetic_samples.py -f intent_classifier_samples.csv -l 0
# done


for label in {1..8}; do
    echo "Label: $label"
    for i in {1..10}; do
        python3 generate_synthetic_samples.py -f intent_classifier_samples.csv -l "$label"
        echo "Iteration $i"
    done
done