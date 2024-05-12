class Constraint:
    """Constraint object, helping filter Query results."""
    def __init__(self, key: str, value: str, relation: str, isNumeric: bool = False, decapitalize: bool = False) -> None:
        """Constraint constructor.

        Arguments:
        ----------
        key: str            -- name of Record attribute
        value: str          -- value of corresponding "key" attribute
        relation: str       -- relation (equal, nonequal, etc., listed below)
        isNumeric: bool     -- if True, program will ensure this str contains only numbers
        decapitalize: bool  -- if True, program will lower CAPS in Record value and Constraint value

        Relations:
        ----------
        eq      -- values are equal
        nq      -- values are not equal
        gt / qe -- record value is greater / greater or equal than constraint value
        lt / le -- record value is lesser / lesser or equal than constraint value
        in      -- constraint value is in record value
        """

        self.key = key
        self.value = value
        self.relation = relation
        self.isNumeric = isNumeric
        self.decapitalize = decapitalize  