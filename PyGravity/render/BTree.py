#!/usr/bin/env python3
'''
Created on 20200211
Update on 20200611
@author: Eduardo Pagotto
 '''

class Node:
    def __init__(self, val):
        self.value = val
        self.leftChild = None
        self.rightChild = None

    def insert(self, data):
        if self.value == data:
            return False
        elif self.value > data:
            if self.leftChild:
                return self.leftChild.insert(data)
            else:
                self.leftChild = Node(data)
                return True
        else:
            if self.rightChild:
                return self.rightChild.insert(data)
            else:
                self.rightChild = Node(data)
                return True

    def find(self, data):
        if self.value == data:
            return True
        elif self.value > data:
            if self.leftChild:
                return self.leftChild.find(data)
            else:
                return False
        else:
            if self.rightChild:
                return self.rightChild.find(data)
            else:
                return False


    def preorder(self):

        print(str(self.value))

        if self.leftChild:
            self.leftChild.preorder()

        if self.rightChild:
            self.rightChild.preorder()

    def postorder(self):

        if self.leftChild:
            self.leftChild.postorder()

        if self.rightChild:
            self.rightChild.postorder()

        print(str(self.value))

    def inorder(self):

        if self.leftChild:
            self.leftChild.inorder()

        print(str(self.value))

        if self.rightChild:
            self.rightChild.inorder()


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root:
            return self.root.insert(data)
        else:
            self.root = Node(data)
            return True

    def find(self, data):
        if self.root:
            return self.root.find(data)
        else:
            return False

    def preorder(self):
        print('preorder')
        self.root.preorder()


    def postorder(self):
        print('postorder')
        self.root.postorder()


    def inorder(self):
        print('inorder')
        self.root.inorder()

def getLeafCount(node):

    if node is None:
        return 0

    if (node.leftChild is None) and (node.rightChild is None):
        return 1
    else:
        return getLeafCount(node.leftChild) + getLeafCount(node.rightChild)


if __name__ == '__main__':

    bt = Tree()
    bt.insert(10)
    bt.insert(5)
    bt.insert(12)
    bt.insert(15)
    bt.insert(1)
    bt.insert(7)
    bt.insert(9)
    bt.insert(14)
    bt.insert(0)
    bt.insert(6)
    bt.insert(16)
    bt.insert(11)
    bt.insert(2)

    val = getLeafCount(bt.root)


    bt.preorder()
    bt.postorder()
    bt.inorder()