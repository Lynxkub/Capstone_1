

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
        // card styling not correct when added dynamically. Spacing is weird. Not sure why yet?
}

$('#add_menu_item').click(addMenuItem)


//  async function patch_actuals(e){
//      e.preventDefault();
//     const id = $(this).data('id');
//     let monday = $('#monday').val();
//     let tuesday = $('#tuesday').val();
//     let wednesday = $('#wednesday').val();
//     let thursday = $('#thursday').val();
//     let friday = $('#friday').val();
//     let saturday = $('#saturday').val();
//     let sunday = $('#sunday').val();

//     // let weekly_total = monday + tuesday + wednesday + thursday + friday + saturday + sunday;
    
//     actuals = await axios.delete(`/api/actuals`, {monday, tuesday, wednesday, thursday, friday, saturday, sunday});
    
// }

// $('#actuals_submit').click(patch_actuals)