

async function deleteMenu(){
    const id = $(this).data('id')
    console.log(id)
    await axios.delete(`/api/menu/${id}`)
    $(this).parent().remove()
}

$('.menu_delete_button').click(deleteMenu)

async function addMenuItem(e){
    e.preventDefault();
    let menu_id = $(this).data('id')
    
    let menu_item_name =  $('#menu_item_name').val();
    let menu_description = $('#menu_description').val();
    let menu_price = $('#menu_price').val();
    let forwardSlash = '/'
    const menu_item = await axios.post(`/new_menu_items/${menu_id}`, {menu_item_name, menu_description, menu_price})
    
    $('#menu_item_name').val('');
    $('#menu_description').val('');
    $('#menu_price').val('');
    $('#menu_list').append(
        `<div class = 'card' style = 'width: 18rem;>
        
            <div class = 'card-body'>
                <h5 class = 'card-title'>${menu_item_name}</h5>
                <h6 class = 'card-subtitle mb=2 text-muted'>${menu_description}</h6>
                <h6 class = 'card-subtitle mb=2 text-muted'>${menu_price}</h6>
        </div>
        
        </div>`)
        // card styling not correct when added dynamically. Spacing is weird. Not sure why yet? Also, need to add a link. How do I escape a forward slash (/) in order to create a link to flask app?
}

$('#add_menu_item').click(addMenuItem)




async function delete_ingredient(){
    const id = $(this).data('id');
    console.log(id)
    await axios.delete(`/api/delete_product/${id}`);
    $(this).parent().remove();
}

$('.item_delete_button').click(delete_ingredient)