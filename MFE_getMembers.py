
from RFEM.enums import ObjectTypes
from RFEM.initModel import Model
from RFEM.BasicObjects.member import Member
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType

def getMembers(model = Model):
    MemberNumbers = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_MEMBER,model)
    members = []
    for n in MemberNumbers:
        member = Member.GetMember(n,model)
        members.append({"no":member.no,"startNode": member.node_start, "endNode":member.node_end, "line": member.line})
    return members
