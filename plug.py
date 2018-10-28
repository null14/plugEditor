from maya.api import OpenMaya as om

sList = om.MGlobal.getActiveSelectionList()

node = NodePlug("pSphere1")
plug = node.find_plug("rotate")
plug.source()
plug.destinations()
plugs = node.plugs()

print node.destinations(0)[0].name()
print node.destinations(1)[0].name()

print node.sources(0)[0].name()
print node.sources(1)[0].name()


srcnodes = node.source_nodes()
destnodes = node.destination_nodes()

srcnodes[0].plugs()

pplug = plug.parent()
aplug = AttrPlug(plug)
aplug.attr.keyable

class NodePlug:
    def __init__(self, node=""):
        if isinstance(node, str):
            self.selnode = om.MGlobal.getSelectionListByName(node)
            self.mobject = self.selnode.getDependNode(0)
        elif isinstance(node, om.MObject):
            self.mobject = node
        self.dependency = om.MFnDependencyNode(self.mobject)

    def name(self):#str
        return self.dependency.name()

    def find_plug(self, attrname):#MPlug
        return self.dependency.findPlug(attrname, False)

    def sources(self,connections=0):#[MPlug]
        return self.connected_all(1,0,connections)

    def source_nodes(self):#[NodePlug]
        result = []
        for plug in self.sources():
            result.append(NodePlug(plug.node()))
        return result

    def destinations(self, connections=0):#[MPlug]
        return self.connected_all(0,1,connections)

    def destination_nodes(self):#[NodePlug]
        result = []
        for plug in self.destinations():
            result.append(NodePlug(plug.node()))
        return result
                
    def plugs(self):#[MPlug]
        results = []
        count = self.dependency.attributeCount()
        for i in xrange(count):
            attrObj = self.dependency.attribute(i)
            plug    = self.find_plug(attrObj)
            results.append(plug)
            #print plug.partialName(True, True, True, False, True, True)
        return results
            
    def connected_all(self, source=0, destination=0, connections=0):#[MPlug]
        results = []
        for plug in self.plugs():
            for cnct in plug.connectedTo(source,destination):
                if connections:
                    results.append(plug)
                else:
                    results.append(cnct)
        return results


class AttrPlug:
    def __init__(self, mplug):
        if isinstance(mplug, om.MPlug):
            self.mobject = mplug.attribute()
        elif isinstance(mplug, om.MObject):
            self.mobject = mplug
        self.attr = om.MFnAttribute(self.mobject)

    def attribute(self):
        return self.mfnattr