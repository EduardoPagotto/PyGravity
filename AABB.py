#!/usr/bin/env python3
'''
Created on 20191105
Update on 20191107
@author: Eduardo Pagotto
 '''

# ref: https://www.azurefromthetrenches.com/introductory-guide-to-aabb-tree-collision-detection/

import glm
from collections import deque

class AABB(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.size = max - min # [glm.vec3] -- [Width:x; Height:y; Depth:z]
        self.surfaceArea = 2.0 * (self.size.x * self.size.y + self.size.x * self.size.z + self.size.y * self.size.z)

    def _v3(self, val):
        return '({0:.2f} {1:.2f} {2:.2f})'.format(val.x, val.y, val.z)

    def __str__(self):
        return 'MIN:{0} MAX:{1} SIZE:{2} A:{3}'.format(self._v3(self.min), self._v3(self.max), self._v3(self.size), self.surfaceArea)

    def overlaps(self, other): 
        return (self.max.x > other.min.x and
                self.min.x < other.max.x and
                self.max.y > other.min.y and
                self.min.y < other.max.y and
                self.max.z > other.min.z and
                self.min.z < other.max.z)

    def contains(self, other):
        return (other.min.x >= self.min.x and
                other.max.x <= self.max.x and
                other.min.y >= self.min.y and
                other.max.y <= self.max.y and
                other.min.z >= self.min.z and
                other.max.z <= self.max.z)
	
    def merge(self, other):
        return AABB(glm.min(self.min, other.min), glm.max(self.max, other.max))

    def intersection(self, other):
        return AABB(glm.min(self.max, other.max), glm.max(self.min, other.min))

    def transformation(self, trans):
        # FIXME: esta errado!!!!
        self.min = glm.vec3(trans * glm.vec4(self.min, 1.0))
        self.max = glm.vec3(trans * glm.vec4(self.max, 1.0))

# AABB AABB::transformation(const glm::mat4& transformation) {

#     glm::vec3 val, min, max;
#     for (short i = 0; i < 8; i++) {
#         val = glm::vec3(transformation * glm::vec4(vertices[i], 1.0f));
#         if (i != 0) {
#             min = glm::min(min, val);
#             max = glm::max(max, val);
#         } else {
#             min = val;
#             max = val;
#         }
#     }

   



AABB_NULL_NODE = -1

class AABBNode(object):
    def __init__(self):
        self.aabb = None
        #std::shared_ptr<IAABB> object;
        self.parent = AABB_NULL_NODE
        self.left = AABB_NULL_NODE
        self.right = AABB_NULL_NODE
        self.next = AABB_NULL_NODE

    def isLeaf(self):
        return self.left == AABB_NULL_NODE

    def __str__(self):
        return '{0} ^:{1}, <:{2}, >:{3}, next:{4}'.format(self.aabb,
                                                            self.parent,
                                                            self.left,
                                                            self.right,
                                                            self.next)

class AABBTree(object):
    def __init__(self, initialSize):

        self._objectNodeIndexMap = []

        self._nodes = [] 
        self._root = AABB_NULL_NODE
        self._allocated = 0
        self._nextFree = 0
        self._capacity = initialSize
        self._growthSize = initialSize

        for nodeIndex in range(0, initialSize):
            node = AABBNode()
            node.next = nodeIndex + 1
            self._nodes.append(node)

        if initialSize > 0:
            self._nodes[initialSize-1].next = AABB_NULL_NODE

    def debug(self):
       self.debug_data(self._root)
        
    def debug_data(self, indiceNode):

        if indiceNode == AABB_NULL_NODE:
            return

        node = self._nodes[indiceNode]

        if node.left == AABB_NULL_NODE and node.right == AABB_NULL_NODE:
            print('Leaf:{0}-{1}'.format(indiceNode, node))
        else:
            print('Node:{0}-{1}'.format(indiceNode, node))

        if node.left != AABB_NULL_NODE:
            self.debug_data(node.left)

        if node.right != AABB_NULL_NODE:
            self.debug_data(node.right)

    def allocateNode(self):
        if self._nextFree == AABB_NULL_NODE:
            self._capacity += self._growthSize
            for nodeIndex in range(self._allocated, self._capacity):            
                node = AABBNode()
                self._nodes.append(node)
                node.next = nodeIndex + 1
            
            self._nodes[self._capacity - 1].next = AABB_NULL_NODE
            self._nextFree = self._allocated

        nodeIndex = self._nextFree
        allocatedNode = self._nodes[nodeIndex]
        allocatedNode.parent = AABB_NULL_NODE
        allocatedNode.left = AABB_NULL_NODE
        allocatedNode.right = AABB_NULL_NODE
        self._nextFree = allocatedNode.next
        self._allocated+=1
        return nodeIndex
      
    def deallocateNode(self, nodeIndex):
        deallocatedNode = self._nodes[nodeIndex]
        deallocatedNode.next = self._nextFree
        self._nextFree = nodeIndex
        self._allocated-=1

    def insertLeaf(self, leafNodeIndex):

        if self._root == AABB_NULL_NODE:
        	self._root = leafNodeIndex
        	return
        
        treeNodeIndex = self._root
        leafNode = self._nodes[leafNodeIndex]
        while self._nodes[treeNodeIndex].isLeaf() is False:
        
        	# because of the test in the while loop above we know we are never a leaf inside it
        	treeNode = self._nodes[treeNodeIndex]
        	left = treeNode.left
        	right = treeNode.right
        	leftNode = self._nodes[left]
        	rightNode = self._nodes[right]
        	combinedAabb = treeNode.aabb.merge(leafNode.aabb)

        	newParentNodeCost = 2.0 * combinedAabb.surfaceArea
        	minimumPushDownCost = 2.0 * (combinedAabb.surfaceArea - treeNode.aabb.surfaceArea)

        	# use the costs to figure out whether to create a new parent here or descend
        	costLeft = 0.0
        	costRight = 0.0
        	if leftNode.isLeaf():
        		costLeft = leafNode.aabb.merge(leftNode.aabb).surfaceArea + minimumPushDownCost
        	else:        	
        		newLeftAabb = leafNode.aabb.merge(leftNode.aabb)
        		costLeft = (newLeftAabb.surfaceArea - leftNode.aabb.surfaceArea) + minimumPushDownCost	
        	
        	if rightNode.isLeaf():
        		costRight = leafNode.aabb.merge(rightNode.aabb).surfaceArea + minimumPushDownCost
        	else:
        		newRightAabb = leafNode.aabb.merge(rightNode.aabb)
        		costRight = (newRightAabb.surfaceArea - rightNode.aabb.surfaceArea) + minimumPushDownCost
        	
        	# if the cost of creating a new parent node here is less than descending in either direction then
        	# we know we need to create a new parent node, errrr, here and attach the leaf to that
        	if (newParentNodeCost < costLeft and newParentNodeCost < costRight):
        		break
    
        	# otherwise descend in the cheapest direction
        	if costLeft < costRight:
        		treeNodeIndex = left
        	else:
        		treeNodeIndex = right
        
        # the leafs sibling is going to be the node we found above and we are going to create a new
        # parent node and attach the leaf and this item
        leafSiblingIndex = treeNodeIndex
        leafSibling = self._nodes[leafSiblingIndex]
        oldParentIndex = leafSibling.parent
        newParentIndex = self.allocateNode()
        newParent = self._nodes[newParentIndex]
        newParent.parent = oldParentIndex
        newParent.aabb = leafNode.aabb.merge(leafSibling.aabb) # the new parents aabb is the leaf aabb combined with it's siblings aabb
        newParent.left = leafSiblingIndex
        newParent.right = leafNodeIndex
        leafNode.parent = newParentIndex
        leafSibling.parent = newParentIndex

        if oldParentIndex == AABB_NULL_NODE:
        	# the old parent was the root and so this is now the root
        	self._root = newParentIndex
        else:
        	# the old parent was not the root and so we need to patch the left or right index to
        	# point to the new node
        	oldParent = self._nodes[oldParentIndex]
        	if oldParent.left == leafSiblingIndex:
        		oldParent.left = newParentIndex
        	else:
        		oldParent.right = newParentIndex
        
        # finally we need to walk back up the tree fixing heights and areas
        treeNodeIndex = leafNode.parent
        self.fixUpwardsTree(treeNodeIndex)

    def removeLeaf(self, leafNodeIndex):
        # if the leaf is the root then we can just clear the root pointer and return
        if (leafNodeIndex == self._root):
        	self._root = AABB_NULL_NODE
        	return
        
        leafNode = self._nodes[leafNodeIndex]
        parent = leafNode.parent
        parentNode = self._nodes[parent]
        grandparent = parentNode.parent
        siblingNodeIndex = parentNode.right if parentNode.left == leafNodeIndex else parentNode.left
        #assert(siblingNodeIndex != AABB_NULL_NODE); // we must have a sibling
        siblingNode = self._nodes[siblingNodeIndex]
        
        if grandparent != AABB_NULL_NODE:
        
        	# if we have a grand parent (i.e. the parent is not the root) then destroy the parent and connect the sibling to the grandparent in its
        	# place
        	grandParentNode = self._nodes[grandparent]
        	if grandParentNode.left == parent:
        		grandParentNode.left = siblingNodeIndex
        	else:
        		grandParentNode.right = siblingNodeIndex

        	siblingNode.parent = grandparent
        	self.deallocateNode(parent)

        	self.fixUpwardsTree(grandparent)
        
        else:
        	# if we have no grandparent then the parent is the root and so our sibling becomes the root and has it's parent removed
        	self._root = siblingNodeIndex
        	siblingNode.parent = AABB_NULL_NODE
        	self.deallocateNode(parent)
        
        leafNode.parent = AABB_NULL_NODE

    def updateLeaf(self, leafNodeIndex, newAaab):
        node = self._nodes[leafNodeIndex]
        
        # if the node contains the new aabb then we just leave things
        # TODO: when we add velocity this check should kick in as often an update will lie within the velocity fattened initial aabb
        # to support this we might need to differentiate between velocity fattened aabb and actual aabb
        if node.aabb.contains(newAaab):
            return

        self.removeLeaf(leafNodeIndex)
        node.aabb = newAaab
        self.insertLeaf(leafNodeIndex)
        
    def fixUpwardsTree(self, treeNodeIndex):
        while treeNodeIndex != AABB_NULL_NODE:
        
            treeNode = self._nodes[treeNodeIndex]

            leftNode = self._nodes[treeNode.left]
            rightNode = self._nodes[treeNode.right]
            treeNode.aabb = leftNode.aabb.merge(rightNode.aabb)

            treeNodeIndex = treeNode.parent
        
    def insertAABB(self, aabb):
        nodeIndex = self.allocateNode()
        node = self._nodes[nodeIndex]
        node.aabb = aabb
        self.insertLeaf(nodeIndex)
        self._objectNodeIndexMap.append((aabb, nodeIndex))

    # TODO: Testar
    def removeObject(self, aabb): 
        for item in self._objectNodeIndexMap:
            if item[0]==aabb:
                indice = item[1]
                self.removeLeaf(indice)
                self.deallocateNode(indice)
                self._objectNodeIndexMap.remove(item)
                break

    # TODO: Testar
    def updateObject(self, aabb):
        for item in self._objectNodeIndexMap:
            if item[0]==aabb:
                indice = item[1]
                self.updateLeaf(indice, aabb)

    # TODO: testar
    def queryOverlaps(self, testAabb):
        overlaps = [] 
        stack = deque() 
        stack.append(self._root) 
        while len(stack) > 0:

            nodeIndex = stack.pop()
            if nodeIndex == AABB_NULL_NODE:
                continue

            node = self._nodes[nodeIndex]
            if node.aabb.overlaps(testAabb):
                if (node.isLeaf() and node.aabb != testAabb):
                    overlaps.append(node.testAabb)
                else:
                    stack.append(node.leftNodeIndex)
                    stack.append(node.rightNodeIndex)
        		
        return overlaps

if __name__ == '__main__':


    t = AABBTree(20)

    q1 = AABB(glm.vec3(1,1,0), glm.vec3(2,2,0))
    t.insertAABB(q1)

    q2 = AABB(glm.vec3(3,3,0), glm.vec3(4,4,0))
    t.insertAABB(q2)

    q3 = AABB(glm.vec3(5,5,0), glm.vec3(6,6,0))
    t.insertAABB(q3)

    q4 = AABB(glm.vec3(-10,-10,0), glm.vec3(-5,-5,0))
    t.insertAABB(q4)

    q5 = AABB(glm.vec3(7,-6,0), glm.vec3(9,-4,0))
    t.insertAABB(q5)

    t.debug()


    print('fim')
