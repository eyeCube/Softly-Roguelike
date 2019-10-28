// Starter file for doubly-linked list.  templated Node class
// each Node stores a piece of data, along with prev and next pointers
// to point to the previous and the next nodes in the list, respectively

#include <utility>

template <typename T>	class TList;		// forward declaration
template <typename T>	class TListIterator;	// forward declaration

// declaration of Node class

template <typename T>
class Node
{
   friend class TList<T>;
   friend class TListIterator<T>;
public:
   Node(const T& d);
   Node(T && d);
 
private:
   T data;		// data element to store
   Node<T> * prev;	// pointer to previous node
   Node<T> * next;	// pointer to next node
};

// Node constructor definitions

template <typename T>
Node<T>::Node(const T& d)
// copy version
{
   data = d;				// set data
   prev = next = nullptr;		// null pointers to start
}

template <typename T>
Node<T>::Node(T && d)
// MOVE version (if applicable for type T)
{
   data = std::move(d);			// set data
   prev = next = nullptr;		// null pointers to start
}