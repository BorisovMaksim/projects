#include <vector>
#include <iostream>
#include <set>
#include <algorithm>

using namespace std;


void print_vector_of_vector(const vector<vector<int>> & v){
        for (auto const &vect: v) {
            cout << "{ ";
            for (auto elem: vect)
                cout << elem << " ";
            cout << "}  ";
        }
}
void print_set_of_vector_of_vector(const set<vector<vector<int>>> &s){
                for (auto it=s.begin(); it != s.end(); ++it) {
                    cout << "{ ";
                    print_vector_of_vector(*it);
                    cout << " } \n";
            }
}
void generate_integration(const vector<vector<int>> & vectors, set<vector<vector<int>>> & s){
    s.insert(vectors);
    for (int i = 0; i < vectors.size() - 1; ++i) {
        for (int j = i + 1; j < vectors.size(); ++j) {
            vector<vector<int>> temp = vectors;
            transform(temp[j].begin( ), temp[j].end( ), temp[i].begin( ), temp[j].begin( ),plus<>( ));
            temp.erase(temp.begin() + i);
            s.insert(temp);
            generate_integration(temp, s);
        }
    }

}

set<vector<vector<int>>> find_suitable_integrations(const vector<vector<vector<int>>> & vector_of_integration){
    set<vector<vector<int>>> intersect;
    generate_integration(vector_of_integration[0], intersect);
    for (int i = 1; i < vector_of_integration.size(); ++i) {
        set<vector<vector<int>>> intersect_temp;
        set<vector<vector<int>>> temp_set;
        generate_integration(vector_of_integration[i], temp_set);
        set_intersection(temp_set.begin(),temp_set.end(),intersect.begin(),intersect.end(),
                         inserter(intersect_temp, intersect_temp.begin()));
        intersect = intersect_temp;
    }
    return intersect;
}




int main(){
    int num_integrations = 0;
    int sz = 0;
    cout << "Введите количество вписываний в конфигурации\n";
    cin >> num_integrations;
    cout << "Введите фиксированный размер векторов\n";
    cin >> sz;
    cout << "Необходимо ввести " << num_integrations <<" прообраза\n";
    vector<vector<vector<int>>>  vector_of_integration;
    for (int i = 0; i < num_integrations; ++i) {
        vector<vector<int>> vec_to_push;
        int num_v = 0;
        cout << "Введите количество векторов в прообразе " << i + 1<<"\n";
        cin >> num_v;
        for (int k = 0; k < num_v; ++k) {
            cout << "Введите вектор под номером "<< k + 1<<"\n";
            vector<int> x;
            int y;
            for (int j = 0; j < sz; ++j) {
                cin >> y;
                x.push_back(y);
            }
            vec_to_push.push_back(x);

        }
        vector_of_integration.push_back(vec_to_push);
    }
    cout << "Введите количество векторов в образе вписываний\n";
    int num_v = 0;
    cin >> num_v;
    vector<vector<int>> c;
    for (int k = 0; k < num_v; ++k) {
        cout << "Введите вектор под номером "<< k + 1 <<"\n";
        vector<int> x;
        int y;
        for (int j = 0; j < sz; ++j) {
            cin >> y;
            x.push_back(y);
        }
        c.push_back(x);
    }
    set<vector<vector<int>>>  set_of_integration = find_suitable_integrations(vector_of_integration);
    vector<vector<int>> min_integration = c;
    for (const auto & integration: set_of_integration){
        set<vector<vector<int>>> temp_set;
        generate_integration(integration,temp_set);
        if (temp_set.find(min_integration) != temp_set.end())
            min_integration = integration;
    }
    cout << "Образ вписываний в минимальной кофигурации \n";
    print_vector_of_vector(min_integration);

}

