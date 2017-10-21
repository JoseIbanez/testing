
@L CUST-66
changeto context CUST-066-CE-CONTEXT-SPE01
terminal pager 0

@L CUST-66-show_run-PRE
show run 

@L CUST-66-config
conf t
end
wr

@L CUST-66-show_run-POST
show run 




@L Admin
changeto context ADMIN-CONTEXT
terminal pager 0

show ver

conf t
end


