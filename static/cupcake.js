
function generateCupcakeHTML(cupcake) {
    return `<div id=${cupcake.id}>
        <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button" >X</button>
        </li>
        <img class="cupcake-image" src="${cupcake.image} " alt="no image provided" width="250" height="180"/>
    </div>`;
};

async function getCupcakeList(){
    const response = await axios.get('/api/cupcakes');
    for(let cupcake of response.data.cupcakes) {
        let newCupcake = generateCupcakeHTML(cupcake);
        $(".cupcakes-list").append(newCupcake);
    }
};


$('.add-cupcake').submit('button',addCupcake);

async function addCupcake(e){
    e.preventDefault();
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

   const response = await axios.post('/api/cupcakes', {flavor,rating,size,image});

   let newCupcake = generateCupcakeHTML(response.data.cupcake);
   $(".cupcakes-list").append(newCupcake);
   $(".add-cupcake").trigger("reset");
};

$('ul').click('button',deleteCupcake);

async function deleteCupcake(e){
    // alert('you clicked!')
    e.preventDefault();
    console.log(e);
    let $div = e.target.closest('div');
    let cupcakeId = ($div.id);
    // let $div = e.closest('div'); // let $div = $(e.target).closest('div')
    // let cupcakeId = e.data('cupcake-id');

    await axios.delete(`/api/cupcakes/${cupcakeId}`); //dont need a response here
    
    $div.remove();

}

$(getCupcakeList);