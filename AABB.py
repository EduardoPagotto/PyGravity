#!/usr/bin/env python3
'''
Created on 20191105
Update on 20191105
@author: Eduardo Pagotto
 '''

# ref: https://www.azurefromthetrenches.com/introductory-guide-to-aabb-tree-collision-detection/

import glm

class AABB(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.size = max - min # [glm.vec3] -- [Width:x; Height:y; Depth:z]
        self.surfaceArea = 2.0 * (self.size.x * self.size.y + self.size.x * self.size.z + self.size.y * self.size.z)

    def __str__(self):
        return 'MIN:{0} MAX:{1}'.format(self.min, self.max)

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

AABB_NULL_NODE = -1

class AABBNode(object):
    def __init__(self):
        self.aabb = None
        #std::shared_ptr<IAABB> object;
        self.parentNodeIndex = AABB_NULL_NODE
        self.leftNodeIndex = AABB_NULL_NODE
        self.rightNodeIndex = AABB_NULL_NODE
        self.nextNodeIndex = AABB_NULL_NODE

    def isLeaf(self):
        return self.leftNodeIndex == AABB_NULL_NODE

class AABBTree(object):
    def __init__(self, initialSize):

        self._objectNodeIndexMap = []

        self._nodes = [] 
        self._rootNodeIndex = AABB_NULL_NODE
        self._allocatedNodeCount = 0
        self._nextFreeNodeIndex = 0
        self._nodeCapacity = initialSize
        self._growthSize = initialSize

        for nodeIndex in range(0, initialSize):
            node = AABBNode()
            node.nextNodeIndex = nodeIndex + 1
            self._nodes.append(node)

        if initialSize > 0:
            self._nodes[initialSize-1].nextNodeIndex = AABB_NULL_NODE

    def allocateNode(self):
        if self._nextFreeNodeIndex == AABB_NULL_NODE:
            self._nodeCapacity += self._growthSize
            #_nodes.resize(_nodeCapacity);
            for nodeIndex in range(self._allocatedNodeCount, self._nodeCapacity):            
                node = AABBNode()
                self._nodes.append(node)
                node.nextNodeIndex = nodeIndex + 1
            
            self._nodes[self._nodeCapacity - 1].nextNodeIndex = AABB_NULL_NODE
            self._nextFreeNodeIndex = self._allocatedNodeCount

        nodeIndex = self._nextFreeNodeIndex
        allocatedNode = self._nodes[nodeIndex]
        allocatedNode.parentNodeIndex = AABB_NULL_NODE
        allocatedNode.leftNodeIndex = AABB_NULL_NODE
        allocatedNode.rightNodeIndex = AABB_NULL_NODE
        self._nextFreeNodeIndex = allocatedNode.nextNodeIndex
        self._allocatedNodeCount+=1
        return nodeIndex
      
    def deallocateNode(self, nodeIndex):
        deallocatedNode = self._nodes[nodeIndex]
        deallocatedNode.nextNodeIndex = self._nextFreeNodeIndex
        self._nextFreeNodeIndex = nodeIndex
        self._allocatedNodeCount-=1

    def insertLeaf(self, leafNodeIndex):

        if self._rootNodeIndex == AABB_NULL_NODE:
        	self._rootNodeIndex = leafNodeIndex
        	return
        
        treeNodeIndex = self._rootNodeIndex
        leafNode = self._nodes[leafNodeIndex]
        while self._nodes[treeNodeIndex].isLeaf() is False:
        
        	# because of the test in the while loop above we know we are never a leaf inside it
        	treeNode = self._nodes[treeNodeIndex]
        	leftNodeIndex = treeNode.leftNodeIndex
        	rightNodeIndex = treeNode.rightNodeIndex
        	leftNode = self._nodes[leftNodeIndex]
        	rightNode = self._nodes[rightNodeIndex]
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
        		treeNodeIndex = leftNodeIndex
        	else:
        		treeNodeIndex = rightNodeIndex
        
        # the leafs sibling is going to be the node we found above and we are going to create a new
        # parent node and attach the leaf and this item
        leafSiblingIndex = treeNodeIndex
        leafSibling = self._nodes[leafSiblingIndex]
        oldParentIndex = leafSibling.parentNodeIndex
        newParentIndex = self.allocateNode()
        newParent = self._nodes[newParentIndex]
        newParent.parentNodeIndex = oldParentIndex
        newParent.aabb = leafNode.aabb.merge(leafSibling.aabb) # the new parents aabb is the leaf aabb combined with it's siblings aabb
        newParent.leftNodeIndex = leafSiblingIndex
        newParent.rightNodeIndex = leafNodeIndex
        leafNode.parentNodeIndex = newParentIndex
        leafSibling.parentNodeIndex = newParentIndex

        if (oldParentIndex == AABB_NULL_NODE):
        	# the old parent was the root and so this is now the root
        	_rootNodeIndex = newParentIndex
        else:
        	# the old parent was not the root and so we need to patch the left or right index to
        	# point to the new node
        	oldParent = self._nodes[oldParentIndex]
        	if oldParent.leftNodeIndex == leafSiblingIndex:
        		oldParent.leftNodeIndex = newParentIndex
        	else:
        		oldParent.rightNodeIndex = newParentIndex
        
        # finally we need to walk back up the tree fixing heights and areas
        treeNodeIndex = leafNode.parentNodeIndex
        self.fixUpwardsTree(treeNodeIndex)

    def removeLeaf(self, leafNodeIndex):
        # if the leaf is the root then we can just clear the root pointer and return
        if (leafNodeIndex == self._rootNodeIndex):
        	self._rootNodeIndex = AABB_NULL_NODE
        	return
        

        leafNode = self._nodes[leafNodeIndex]
        parentNodeIndex = leafNode.parentNodeIndex
        parentNode = self._nodes[parentNodeIndex]
        grandParentNodeIndex = parentNode.parentNodeIndex
        siblingNodeIndex = parentNode.rightNodeIndex if parentNode.leftNodeIndex == leafNodeIndex else parentNode.leftNodeIndex
        #assert(siblingNodeIndex != AABB_NULL_NODE); // we must have a sibling
        siblingNode = self._nodes[siblingNodeIndex]
        
        if grandParentNodeIndex != AABB_NULL_NODE:
        
        	# if we have a grand parent (i.e. the parent is not the root) then destroy the parent and connect the sibling to the grandparent in its
        	# place
        	grandParentNode = self._nodes[grandParentNodeIndex]
        	if grandParentNode.leftNodeIndex == parentNodeIndex:
        		grandParentNode.leftNodeIndex = siblingNodeIndex
        	else:
        		grandParentNode.rightNodeIndex = siblingNodeIndex

        	siblingNode.parentNodeIndex = grandParentNodeIndex
        	self.deallocateNode(parentNodeIndex)

        	self.fixUpwardsTree(grandParentNodeIndex)
        
        else:
        	# if we have no grandparent then the parent is the root and so our sibling becomes the root and has it's parent removed
        	_rootNodeIndex = siblingNodeIndex
        	siblingNode.parentNodeIndex = AABB_NULL_NODE
        	self.deallocateNode(parentNodeIndex)
        
        leafNode.parentNodeIndex = AABB_NULL_NODE

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

            leftNode = self._nodes[treeNode.leftNodeIndex]
            rightNode = self._nodes[treeNode.rightNodeIndex]
            treeNode.aabb = leftNode.aabb.merge(rightNode.aabb)

            treeNodeIndex = treeNode.parentNodeIndex
        
    def insertAABB(self, aabb):
        nodeIndex = self.allocateNode()
        node = self._nodes[nodeIndex]
        node.aabb = aabb
        self.insertLeaf(nodeIndex)
        self._objectNodeIndexMap.append((aabb, nodeIndex))




	# def removeObject(const std::shared_ptr<IAABB>& object):
    #     pass

	# def updateObject(const std::shared_ptr<IAABB>& object):
    #     pass

	#std::forward_list<std::shared_ptr<IAABB>> queryOverlaps(const std::shared_ptr<IAABB>& object) const;

if __name__ == '__main__':


    t = AABBTree(10)

    q1 = AABB(glm.vec3(1,1,0), glm.vec3(2,2,0))
    t.insertAABB(q1)

    q2 = AABB(glm.vec3(3,3,0), glm.vec3(4,4,0))
    t.insertAABB(q2)

    q3 = AABB(glm.vec3(5,5,0), glm.vec3(6,6,0))
    t.insertAABB(q3)

    q4 = AABB(glm.vec3(-10,-10,0), glm.vec3(-5,-5,0))
    t.insertAABB(q4)

    print('fim')

    # novo = t.allocateNode()


    # mundo = AABB()
    # mundo.setMinMax(glm.vec3(-10.0, -10.0, -10.0), glm.vec3(10.0, 10.0, 10.0))
    # t.updateLeaf(novo, mundo)

    # novo2 = t.allocateNode()
    # t1 = AABB()
    # t1.setMinMax(glm.vec3(-30.0, -30.0, -30.0), glm.vec3(-15.0, -15.0, -15.0))
    # t.updateLeaf(novo, t1)

    # print(str(t))