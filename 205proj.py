from math import sqrt
import copy
import random
import csv

def calculate_distance(x, y, features):
    dist = sum((x[feature] - y[feature]) ** 2 for feature in features)
    return sqrt(dist)

def nearest_neighbor(data, label, features):
    correct = 0
    for k in range(len(data)): 
        nearest_dist = float('inf')  # track nearest neighbor distance
        nearest_idx = 0  # track nearest neighbor location

        for i in range(len(data)):  
            if k == i:
                pass
            else:
                dist = calculate_distance(data[i], data[k], features)
                if dist < nearest_dist:
                    nearest_idx = i
                    nearest_dist = dist
        if label[nearest_idx] == label[k]:
            correct += 1

    total = len(data)
    accuracy = (correct / total) * 100
    return accuracy


def forward_feature_selection(instances, targets):
    num_features = len(instances[0])
    selected_features = []
    best_selected_features = []
    best_accuracy = 0.0

    for _ in range(num_features):
        best_feature = None
        curr_feature = None
        curr_accuracy = 0.0
        
        for feature in range(num_features):
            if feature not in selected_features:
                selected_features.append(feature)
                accuracy = nearest_neighbor(instances, targets, selected_features)
                # message = "Using feature(s) {} accuracy is {:.2f}".format(selected_features, accuracy)
                message = "Using feature(s) {} accuracy is {:.2f}".format(
                            ", ".join(str(feature + 1) for feature in selected_features),
                            accuracy
                        )
                print(message)
                
                if accuracy > curr_accuracy:
                    curr_accuracy = accuracy
                    curr_feature = feature
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_feature = feature
                
                selected_features.remove(feature)
        
        if curr_feature is not None:
            print("\n")
            selected_features.append(curr_feature)
            if curr_accuracy < best_accuracy:
                print("(Warning, Accuracy has decreased. Continuing search in case of local maxima)")
            # message = "Feature set {} was best, accuracy is {:.2f}".format(selected_features, curr_accuracy)
            message = "Feature set {} was best, accuracy is {:.2f}".format(
                        ", ".join(str(feature + 1) for feature in selected_features),
                        curr_accuracy
                    )
            print(message)
            print("\n")
        if best_feature is not None:
            best_selected_features.append(best_feature)
    
    # message = "Finish search. The best feature set is {}, which has an accuracy of {:.2f}%".format(best_selected_features, best_accuracy)
    message = "Finish search. The best feature set is {}, which has an accuracy of {:.2f}%".format(
            ", ".join(str(feature + 1) for feature in best_selected_features),
            best_accuracy
        )
    print(message)
    return best_selected_features


def backward_feature_selection(data, labels):
    num_features = len(data[0])
    selected_features = list(range(num_features))  # Start with all features selected
    best_selected_features = list(range(num_features))
    best_accuracy = 0.0

    while len(selected_features) > 1:
        curr_accuracy = 0.0
        curr_feature = None
        worst_feature = None
        
        for feature in selected_features:
            remaining_features = selected_features.copy()
            remaining_features.remove(feature)
            accuracy = nearest_neighbor(data, labels, remaining_features)

            # message = "Using feature(s) {} accuracy is {:.2f}".format(remaining_features, accuracy)
            message = "Using feature(s) {} accuracy is {:.2f}".format(
                        ", ".join(str(feature + 1) for feature in remaining_features),
                        accuracy
                    )
            print(message)

            if accuracy > curr_accuracy:
                curr_accuracy = accuracy
                curr_feature = feature

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                worst_feature = feature
        
        # Remove the feature with the lowest accuracy
        if curr_feature is not None:
            print("\n")
            selected_features.remove(curr_feature)
            if curr_accuracy < best_accuracy:
                print("(Warning, Accuracy has decreased. Continuing search in case of local maxima)")
            # message = "Feature set {} was best, accuracy is {:.2f}".format(selected_features, curr_accuracy)
            message = "Feature set {} was best, accuracy is {:.2f}".format(
                        ", ".join(str(feature + 1) for feature in selected_features),
                        curr_accuracy
                    )
            print(message)
            print("\n")
        
        if worst_feature is not None:
            best_selected_features.remove(worst_feature)
    
    # message = "Finish search. The best feature set is {}, which has an accuracy of {:.2f}%".format(best_selected_features, best_accuracy)
    message = "Finish search. The best feature set is {}, which has an accuracy of {:.2f}%".format(
                ", ".join(str(feature + 1) for feature in best_selected_features),
                best_accuracy
            )
    print(message)
    return best_selected_features
    
def read_data(file_name, label, instances):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line) >= 5:
                label.append(line[4])
                instances.append([float(j) for j in line[:4]])
    return label, instances

def sample_data(instances):
    test_proportion = 0.4
    data = list(zip(labels, instances))
    random.shuffle(data)
    num_test = int(len(data) * test_proportion)
    sample_data = data[num_test:]
    labels, instances = zip(*sample_data)
    return labels, instances


def main():
    print('---------- Welcome to Feature Selection ----------\n')
    labels = []
    instances = []
    file_name = input('Type in the name of the file to test: \n')
    choice = int(input('Type the number of the algorithm you want to run.\n'
                '  1) Forward Selection\n'
                '  2) Backward Elimination\n'))
    if file_name == "data/iris.data":
        labels, instances = read_data(file_name, labels, instances)
    else:
        with open(file_name, 'r') as raw_data:
            for i, line in enumerate(raw_data):
                line = line.strip().split()
                labels.append(float(line[0]))
                instances.append([float(j) for j in line[1:]])

        # sample the data to speed up
        if file_name == "data/xlarge12.txt":
            labels, instances = sample_data
            print("label:", len(labels))
            print("instances:", len(instances))
            print("features:", len(instances[0]))

    feature_number = len(instances[0])
    instance_number = len(instances)
    messg = 'This dataset has {} features (not including the class attribute), with {} instances.\n'.format(feature_number, instance_number)
    print(messg)

    features = [ft for ft in range(feature_number)]
    k_accuracy = nearest_neighbor(instances, labels, features)
    messg = 'Running nearest neighbor with all {} features, using "leaving-one-out" evaluation, I get an accuracy of {}%\n'.format(feature_number, k_accuracy)
    print(messg)

    print('Beginning search.\n')

    if choice == 1:
        forward_feature_selection(instances, labels)
    elif choice == 2:
        backward_feature_selection(instances, labels)

if __name__ == '__main__':
    main()