#include <iostream>
#include <unordered_map>;
#include <unordered_set>
#include <queue>
#include <stack>
#include <vector>
#include <utility>

using namespace std;

// Steam account class
struct steamAccount {

    // Identifiers for the account
    int index;
    int ID;
    string name;
    int numFriends;
    static int maxIndex;

    // Default constructor
    steamAccount();

    // Constructor setting all members
    steamAccount(int ID, string name, int numFriends) {

        this->ID = ID;
        this->index = maxIndex;
        maxIndex++;
        this->name = name;
        this->numFriends = numFriends;

    }

    // Allows comparison of accounts by name
    bool operator==(steamAccount rhs) {

        return ID == ID;

    }

};

// Adjacency List Implementation
class adjacencyListGraph {

    // The graph itself
    unordered_map<steamAccount, vector<steamAccount>> graph;

    // The account the graph is constructed from
    steamAccount source;

public:

    // Public functionality
    adjacencyListGraph(steamAccount source);
    bool FindConnection(steamAccount target);
    void insertEdge(steamAccount from, steamAccount to);
    void printGraph();

};

// Create a graph consisting of the source account, its friends, its friends' friends, and its friends' friends' friends
adjacencyListGraph::adjacencyListGraph(steamAccount source) {

    this->source = source;

}

// Returns whether or not a connection between the two accounts can be established after 3 degrees of separation
bool adjacencyListGraph::FindConnection(steamAccount target) {

    // Perform a breadth-first search (BFS) on the entire graph
    queue<steamAccount> vertices;
    unordered_set<steamAccount> visited;
    int connectionsRequired = 0;

    // Insert the source
    vertices.push(source);
    visited.insert(source);

    // The graph is undirected and connected, so the source will work
    while (!vertices.empty()) {

        // Take out the top of the queue
        steamAccount current = vertices.front();
        vertices.pop();
        vector<steamAccount> children = graph[current];

        // Iterate through its children, look for the target
        for (int i = 0; i < children.size(); i++) {

            // Return true if target is found
            if (children[i] == target) {

                return true;

            }

            // Add any unvisited children to the queue and set
            if (visited.count(children[i]) == 0) {

                visited.insert(children[i]);
                vertices.push(children[i]);

            }

        }

    }

    // All friends up to 3 connections searched, connection not found
    return false;

}


// Inserts an edge (a friendship connection, and possible vertex, an account) into the graph
void adjacencyListGraph::insertEdge(steamAccount from, steamAccount to) {

    // insertEdge() adds a new edge between the from and to vertex
    graph[from].push_back(to);

    // Every vertex should be a key
    if (graph.count(to) == 0) {

        graph[to] = {};

    }

}

// Prints all accounts in the graph, and their friends
void adjacencyListGraph::printGraph() {

    // Perform a depth-first search (DFS) on the entire graph
    stack<steamAccount> vertices;
    unordered_set<steamAccount> visited;
    int connectionsRequired = 0;

    // Insert the source
    vertices.push(source);
    visited.insert(source);

    // The graph is undirected and connected, so the source will work
    while (!vertices.empty()) {

        // Take out the top of the queue and print its values
        steamAccount current = vertices.top();
        cout << current.index << ") Name: " << current.name << " Number of friends: " << current.numFriends << endl;
        vertices.pop();
        vector<steamAccount> children = graph[current];

        // Iterate through its children
        for (int i = 0; i < children.size(); i++) {

            // Add any unvisited children to the queue and set
            if (visited.count(children[i]) == 0) {

                visited.insert(children[i]);
                vertices.push(children[i]);

            }

        }

    }

}

// Adjacency Matrix Implemention
class adjacencyMatrixGraph {

    // The graph itself
    vector<vector<int>> graph;

    // The account the graph is constructed from
    steamAccount source;

    // Maps indices back to their own steamAccount
    unordered_map<int, steamAccount> indices;

public:

    // Public functionality
    adjacencyMatrixGraph(steamAccount source);
    bool FindConnection(steamAccount target);
    void insertEdge(steamAccount from, steamAccount to);
    void printGraph();

};

// Create a graph consisting of the source account, its friends, its friends' friends, and its friends' friends' friends
adjacencyMatrixGraph::adjacencyMatrixGraph(steamAccount source) {

    this->source = source;

}


// Returns whether or not a connection between the two accounts can be established after 3 degrees of separation
bool adjacencyMatrixGraph::FindConnection(steamAccount target) {

    unordered_set<int> visited;


    for (int i = 0; i < graph[0].size(); i++) {



    }

}

// Inserts an edge (a friendship connection, and possible vertex, an account) into the graph
void adjacencyMatrixGraph::insertEdge(steamAccount from, steamAccount to) {

    graph[from.index][to.index] = 1;

}

// Prints all accounts in the graph, and their friends
void adjacencyMatrixGraph::printGraph() {



}

// Client
int main() {

    steamAccount::maxIndex = 0;

    return 0;

}
