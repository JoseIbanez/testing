

CREATE (database:Database {name:"Neo4j"})-[r:SAYS]->(message:Message {name:"Hello World!"}) 
RETURN database, message, r



CREATE (site:Site {name:"Site1"})-[:LIKES]->(company:Company {name:"comp1"}) 
RETURN site, company

CREATE (site:Site {name:"Site2"})-[:LIKES]->(company:Company {name:"comp2"}) 
RETURN site, company


CREATE (site:Site {name:"Site1"})-[:LIKES]->(company:Company {name:"comp2"}) 
RETURN site, company

CREATE (site:Site {name:"Site3"});
CREATE (site:Site {name:"Site4"});

CREATE (c:Company {name:"Company1"});
CREATE (c:Company {name:"Company2"});
CREATE (c:Company {name:"Company3"});
CREATE (c:Company {name:"Company4"});



MATCH (a:Site) RETURN a;
MATCH (b:Company) RETURN b;



MATCH (site:Site {name: 'Site1'})
MATCH (company:Company {name: 'Company1'})
CREATE (site)-[:LIKES]->(company);

MATCH (s:Site)-[r:LIKES]->(c:Company)
RETURN s,r,c;

MATCH (s:Site {name: 'Site1'})
RETURN s;
