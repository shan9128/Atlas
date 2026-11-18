
from day4_member_data import MEMBERS


def lookup_member(member_id):

    member = MEMBERS.get(member_id)

    if member is None:
        return {
            "found": False,
            "member_id": member_id,
            "message": "Member not found"
        }

    return {
        "found": True,
        "member_id": member_id,
        "data": member
    }


if __name__ == "__main__":
    print(lookup_member("M1001"))
    print(lookup_member("M9999"))
